"""PhishGuard — Streamlit front end for the model built in PhishGuard.ipynb.

The notebook writes artifacts/final_model.pkl holding the fitted estimator, the 16
selected features *in training column order*, and the decision threshold. This app
loads all three from that one file rather than restating any of them, so the app and
the notebook cannot drift apart.
"""
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

MODEL_PATH = Path(__file__).parent / 'artifacts' / 'final_model.pkl'

st.set_page_config(page_title='PhishGuard — phishing website detection',
                   page_icon='🛡️', layout='wide')

# --------------------------------------------------------------------------- data
# One entry per selected feature: the question a user answers, and what each of the
# dataset's codes means. Wording follows the rules in "Phishing Websites Features"
# (Mohammad, Thabtah & McCluskey), which is how these columns were originally encoded.
GROUPS = ['Address bar', 'Page contents', 'Domain & reputation']

FEATURE_META = {
    'SSLfinal_State': {
        'group': 'Address bar',
        'label': 'HTTPS certificate',
        'help': 'Trusted issuers include GeoTrust, GoDaddy, Thawte, Comodo, VeriSign. '
                'A certificate under a year old counts as not yet established.',
        'levels': {1: 'HTTPS, trusted issuer, certificate at least 1 year old',
                   0: 'HTTPS, but the issuer is not a trusted authority',
                   -1: 'No HTTPS'},
    },
    'URL_of_Anchor': {
        'group': 'Page contents',
        'label': 'Share of <a> links pointing off-domain or nowhere',
        'help': 'Anchors that link to a different domain, or to "#", "#skip" or '
                '"javascript:void(0)".',
        'levels': {1: 'Under 31%', 0: '31% to 67%', -1: 'Over 67%'},
    },
    'having_Sub_Domain': {
        'group': 'Address bar',
        'label': 'Sub-domains in the address',
        'help': 'Counted after dropping "www." and the country-code suffix.',
        'levels': {1: 'None — e.g. hud.ac.uk', 0: 'One — e.g. mail.hud.ac.uk',
                   -1: 'More than one — e.g. login.mail.hud.ac.uk'},
    },
    'Prefix_Suffix': {
        'group': 'Address bar',
        'label': 'Dash (-) in the domain name',
        'help': 'Phishers add a prefix or suffix separated by a dash, e.g. '
                'confirme-paypal.com.',
        'levels': {1: 'No dash in the domain', -1: 'Domain contains a dash'},
    },
    'web_traffic': {
        'group': 'Domain & reputation',
        'label': 'Traffic rank',
        'levels': {1: 'Ranked in the top 100,000', 0: 'Ranked below 100,000',
                   -1: 'No traffic recorded / not ranked at all'},
    },
    'Links_in_tags': {
        'group': 'Page contents',
        'label': 'Share of <meta>, <script> and <link> tags pointing off-domain',
        'levels': {1: 'Under 17%', 0: '17% to 81%', -1: 'Over 81%'},
    },
    'SFH': {
        'group': 'Page contents',
        'label': 'Where the page submits its forms',
        'help': 'The server form handler — the "action" attribute of a <form>.',
        'levels': {1: 'To the same domain as the page', 0: 'To a different domain',
                   -1: 'Empty, or "about:blank"'},
    },
    'Request_URL': {
        'group': 'Page contents',
        'label': 'Share of images, video and audio loaded from another domain',
        'levels': {1: 'Under 22%', -1: '22% or more'},
    },
    'Links_pointing_to_page': {
        'group': 'Domain & reputation',
        'label': 'External links pointing to this page',
        'levels': {1: 'More than 2', 0: '1 or 2', -1: 'None'},
    },
    'Domain_registeration_length': {
        'group': 'Domain & reputation',
        'label': 'Time until the domain registration expires',
        'help': 'Note: in this dataset the "over a year" level is actually the more '
                'phishing-heavy of the two (60.2% vs 36.4%). The model reflects the '
                'data, not the intuition.',
        'levels': {1: 'More than a year away', -1: 'A year or less'},
    },
    'having_IP_Address': {
        'group': 'Address bar',
        'label': 'IP address used instead of a domain name',
        'help': 'Including hexadecimal forms such as http://0x58.0xCC.0xCA.0x62/.',
        'levels': {1: 'Normal domain name', -1: 'Raw IP address in the URL'},
    },
    'Google_Index': {
        'group': 'Domain & reputation',
        'label': 'Indexed by Google',
        'levels': {1: 'Yes, it appears in search results', -1: 'No'},
    },
    'age_of_domain': {
        'group': 'Domain & reputation',
        'label': 'Age of the domain',
        'levels': {1: '6 months or older', -1: 'Under 6 months'},
    },
    'Statistical_report': {
        'group': 'Domain & reputation',
        'label': 'Listed in PhishTank / StopBadware top-offender reports',
        'help': 'Top 10 phishing domains, top 10 phishing IPs, or StopBadware\'s top 50 IPs.',
        'levels': {1: 'Not listed', -1: 'Host or IP appears in those reports'},
    },
    'Page_Rank': {
        'group': 'Domain & reputation',
        'label': 'PageRank',
        'levels': {1: '0.2 or above', -1: 'Below 0.2'},
    },
    'URL_Length': {
        'group': 'Address bar',
        'label': 'Length of the URL',
        'levels': {1: 'Under 54 characters', 0: '54 to 75 characters',
                   -1: 'Over 75 characters'},
    },
}

# Two ready-made inputs, so the app can be tried without answering 16 questions first.
PRESETS = {
    'A phishing-looking site': {
        'SSLfinal_State': -1, 'URL_of_Anchor': -1, 'having_Sub_Domain': -1,
        'Prefix_Suffix': -1, 'web_traffic': -1, 'Links_in_tags': -1, 'SFH': -1,
        'Request_URL': -1, 'Links_pointing_to_page': -1,
        'Domain_registeration_length': -1, 'having_IP_Address': -1,
        'Google_Index': -1, 'age_of_domain': -1, 'Statistical_report': -1,
        'Page_Rank': -1, 'URL_Length': -1,
    },
    'A legitimate-looking site': {name: 1 for name in FEATURE_META},
    # A real row from the held-out test set (a genuinely legitimate site) that the model
    # scores at 5.2% — just under the warning threshold. Useful because it is the case
    # where the answers actually matter: changing the HTTPS answer alone takes it to 97%.
    'A borderline real site': {
        'SSLfinal_State': 1, 'URL_of_Anchor': 0, 'having_Sub_Domain': 1,
        'Prefix_Suffix': -1, 'web_traffic': 1, 'Links_in_tags': 1, 'SFH': -1,
        'Request_URL': -1, 'Links_pointing_to_page': 1,
        'Domain_registeration_length': 1, 'having_IP_Address': -1,
        'Google_Index': -1, 'age_of_domain': -1, 'Statistical_report': 1,
        'Page_Rank': -1, 'URL_Length': -1,
    },
}


# -------------------------------------------------------------------------- model
@st.cache_resource(show_spinner='Loading the model…')
def load_bundle(path: Path):
    """Load the notebook's artefact. Returns (bundle, error_message)."""
    if not path.exists():
        return None, (f'Model file not found at `{path}`. Run `PhishGuard.ipynb` '
                      'top-to-bottom — section 5.3 writes it — and make sure '
                      '`artifacts/final_model.pkl` is committed alongside `app.py`.')
    try:
        bundle = joblib.load(path)
    except Exception as exc:                                    # unreadable or stale
        return None, (f'The model file could not be loaded: `{exc}`. It is most often '
                      'a scikit-learn version mismatch — install the pinned versions '
                      'with `pip install -r requirements.txt` and re-run the notebook.')
    missing = {'model', 'features', 'threshold', 'phishing_proba_column'} - set(bundle)
    if missing:
        return None, (f'The model file is missing {sorted(missing)}. It was written by '
                      'an older version of the notebook — re-run section 5.3.')
    unknown = [f for f in bundle['features'] if f not in FEATURE_META]
    if unknown:
        return None, (f'The model expects features this app has no questions for: '
                      f'{unknown}. `FEATURE_META` in `app.py` and the notebook\'s '
                      'feature selection have drifted apart.')
    return bundle, None


bundle, error = load_bundle(MODEL_PATH)
if error:
    st.title('🛡️ PhishGuard')
    st.error(error, icon='🚫')
    st.stop()

MODEL = bundle['model']
FEATURES = bundle['features']          # training column order — do not re-sort
THRESHOLD = bundle['threshold']
PHISH_COL = bundle['phishing_proba_column']
META = bundle.get('metadata', {})


def phishing_probability(values: dict) -> float:
    """P(phishing) for one answered form, columns in the order the model was fitted on."""
    row = pd.DataFrame([[values[f] for f in FEATURES]], columns=FEATURES)
    return float(MODEL.predict_proba(row)[0, PHISH_COL])


# ------------------------------------------------------------------------ sidebar
with st.sidebar:
    st.header('About this model')
    st.markdown(
        f"""
        **Gradient boosting**, {len(FEATURES)} features selected from 30.
        Trained on the UCI Phishing Websites dataset (11,055 rows, deduplicated
        to {META.get('n_train', 0) + META.get('n_test', 0):,}).

        A site is flagged when the model's estimated probability reaches
        **{THRESHOLD:.2f}**, not the usual 0.50. That threshold comes from treating one
        missed phishing site as costing **{META.get('fn_to_fp_cost', '?')}×** what one
        false alarm costs — it buys recall by accepting more false alarms.
        """)
    if 'test_recall' in META:
        c1, c2 = st.columns(2)
        c1.metric('Recall (phishing)', f"{META['test_recall']:.1%}",
                  help='Share of phishing sites in the held-out test set that were caught.')
        c2.metric('Precision', f"{META['test_precision']:.1%}",
                  help='Share of flagged sites that really were phishing. '
                       'Lower than recall by design.')
    st.caption(f"Parameters: `{META.get('params', {})}` · `random_state="
               f"{META.get('random_state', '?')}`")
    st.divider()
    st.caption('⚠️ This tool scores **pre-extracted features**, not a live URL. It '
               'cannot visit a website — you describe the site, it estimates the risk. '
               'The training data is a 2015 snapshot; phishing techniques move on.')

# --------------------------------------------------------------------------- form
st.title('🛡️ PhishGuard')
st.write('Answer the questions below about a website. Every answer is one of the '
         'features the model was trained on.')


# Values queued by the "paste codes" form below. They have to be applied here, before
# the selectboxes exist: Streamlit refuses to let a widget's state be reassigned after
# that widget has been created in the same script run.
for feature, code in st.session_state.pop('pending_answers', {}).items():
    st.session_state[f'f_{feature}'] = code


def apply_preset(name: str):
    for feature, code in PRESETS[name].items():
        st.session_state[f'f_{feature}'] = code


def clear_all():
    for feature in FEATURE_META:
        st.session_state[f'f_{feature}'] = None


b1, b2, b3, b4, _ = st.columns([1.25, 1.25, 1.1, 0.6, 1.4])
b1.button('Phishing-looking example', use_container_width=True,
          on_click=apply_preset, args=('A phishing-looking site',))
b2.button('Legitimate-looking example', use_container_width=True,
          on_click=apply_preset, args=('A legitimate-looking site',))
b3.button('Borderline example', use_container_width=True,
          on_click=apply_preset, args=('A borderline real site',))
b4.button('Clear', use_container_width=True, on_click=clear_all)
st.caption('The borderline example is a real site from the held-out test set — the '
           'model puts it at 5.2%, just under the warning threshold. Change its HTTPS '
           'answer to "No HTTPS" and the assessment flips.')

columns = st.columns(len(GROUPS))
for column, group in zip(columns, GROUPS):
    with column:
        st.subheader(group)
        for name in FEATURES:
            meta = FEATURE_META[name]
            if meta['group'] != group:
                continue
            options = [None] + list(meta['levels'])
            st.selectbox(
                meta['label'], options, key=f'f_{name}',
                format_func=lambda code, m=meta: ('— not answered —' if code is None
                                                  else m['levels'][code]),
                help=meta.get('help'))

# ----------------------------------------------------------- advanced / validation
with st.expander('Advanced — paste the 16 feature codes instead'):
    st.caption('For anyone who already has the encoded values: 16 numbers separated by '
               'commas, in the order the model expects. Each must be one of the codes '
               'that feature actually uses (all are −1/1, some also allow 0).')
    st.code(', '.join(FEATURES), language=None)
    pasted = st.text_input('Feature codes', placeholder='-1, 1, 0, -1, …',
                           label_visibility='collapsed')
    if st.button('Apply pasted codes'):
        tokens = [t.strip() for t in pasted.replace(';', ',').split(',') if t.strip()]
        problems = []
        if not tokens:
            problems.append('Nothing was pasted — enter 16 comma-separated codes.')
        elif len(tokens) != len(FEATURES):
            problems.append(f'Expected {len(FEATURES)} values, got {len(tokens)}.')
        else:
            parsed = {}
            for feature, token in zip(FEATURES, tokens):
                try:
                    code = int(token)
                except ValueError:
                    problems.append(f'`{feature}`: "{token}" is not a whole number.')
                    continue
                allowed = sorted(FEATURE_META[feature]['levels'])
                if code not in allowed:
                    problems.append(f'`{feature}`: {code} is not a valid code — '
                                    f'this feature only takes {allowed}.')
                    continue
                parsed[feature] = code
        if problems:
            st.error('Could not read those values:\n\n'
                     + '\n'.join(f'- {p}' for p in problems), icon='🚫')
        else:
            st.session_state['pending_answers'] = parsed
            st.rerun()

# ------------------------------------------------------------------------- result
st.divider()

answers = {name: st.session_state.get(f'f_{name}') for name in FEATURES}
unanswered = [name for name, code in answers.items() if code is None]

if unanswered:
    answered = len(FEATURES) - len(unanswered)
    st.subheader('No assessment yet')
    st.progress(answered / len(FEATURES),
                text=f'{answered} of {len(FEATURES)} questions answered')
    st.info('Answer every question — or load one of the examples above — and the '
            'assessment will appear here and update as you change your answers.',
            icon='ℹ️')
    with st.expander(f'Still to answer ({len(unanswered)})'):
        for name in unanswered:
            st.write(f'- {FEATURE_META[name]["label"]}  ·  *{FEATURE_META[name]["group"]}*')
else:
    probability = phishing_probability(answers)
    is_phishing = probability >= THRESHOLD

    st.subheader('Assessment')
    if is_phishing:
        st.error(f'### ⚠️ Likely phishing\n'
                 f'Estimated probability **{probability:.1%}**, at or above the '
                 f'{THRESHOLD:.0%} threshold for raising a warning.', icon='🚨')
    else:
        st.success(f'### ✅ Likely legitimate\n'
                   f'Estimated probability of phishing is **{probability:.1%}**, below '
                   f'the {THRESHOLD:.0%} warning threshold.', icon='🛡️')

    left, right = st.columns([1, 1])
    with left:
        st.progress(min(probability, 1.0), text=f'P(phishing) = {probability:.1%}')
        st.caption(f'Warning threshold: {THRESHOLD:.0%}. It sits well below 50% on '
                   'purpose — the cost of missing a phishing site is treated as higher '
                   'than the cost of a false alarm, so this model would rather warn '
                   'you unnecessarily than stay quiet.')
        if not is_phishing and probability > THRESHOLD / 2:
            st.warning('This is on the safer side of the threshold, but not by much.',
                       icon='⚠️')

    with right:
        # Local explanation, computed from the model itself: for each answer, how much
        # lower would P(phishing) be if that one answer were its best possible value?
        st.markdown('**What is pushing this score up**')
        deltas = []
        for name in FEATURES:
            best = min(phishing_probability({**answers, name: code})
                       for code in FEATURE_META[name]['levels'])
            deltas.append((probability - best, name))
        deltas.sort(reverse=True)
        top = [(d, n) for d, n in deltas if d > 0.001][:5]
        if not top:
            st.caption('No single answer is carrying this result — it comes from the '
                       'combination.')
        for delta, name in top:
            st.write(f'- **{FEATURE_META[name]["label"]}** — changing this one answer '
                     f'to its safest value would drop the estimate by '
                     f'{delta * 100:.1f} points')

    st.caption('This is a statistical estimate from 16 answers, not a verdict. On the '
               f'held-out test set it caught {META.get("test_recall", 0):.1%} of '
               f'phishing sites, and {1 - META.get("test_precision", 0):.0%} of the '
               'sites it flagged were actually legitimate.')
