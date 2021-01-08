import streamlit as st
from pathlib import Path
from streamlit_player import st_player, _SUPPORTED_EVENTS

import pandas as pd
import re

st.set_page_config(layout="wide")

"""
# 🎬 Streamlit Player [![GitHub][github_badge]][github_link] [![PyPI][pypi_badge]][pypi_link]

[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
[github_link]: https://github.com/okld/streamlit-player

[pypi_badge]: https://badgen.net/pypi/v/streamlit-player?icon=pypi&color=black&label
[pypi_link]: https://pypi.org/project/streamlit-player

---
"""

with st.sidebar:
    "## ⚙️ Parameters"

    options = {
        "events": st.multiselect("Events to listen", _SUPPORTED_EVENTS, ["onProgress"]),
        "progress_interval": st.slider("Progress refresh interval (ms)", 200, 2000, 500, 1),
        "volume": st.slider("Volume", 0.0, 1.0, 1.0, .01),
        "playing": st.checkbox("Playing", False),
        "loop": st.checkbox("Loop", False),
        "controls": st.checkbox("Controls", True),
        "muted": st.checkbox("Muted", False),
    }

    """
    ---
    ## ⏯️ Supported players

    * Dailymotion
    * Facebook
    * Local files
    * Mixcloud
    * SoundCloud
    * Streamable
    * Twitch
    * Vimeo
    * Wistia
    * YouTube
    """

GOOGLE_SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1o_Wijdc84VkeVh5c94h0qKjqZjgRTmZnY7KDqPhNLAk/edit?usp=sharing"
    
# c1, c2 = st.beta_columns(2)

# stcols = dict(c1=c1, c2=c2)




def get_avdata_from_google_spreadsheet(google_spreadsheet_id: str=None, google_spreadsheet_url:str=None, sheet_name = "AVSources"):
    # import pandas as pd
    # import re
    if (google_spreadsheet_url is None) and (google_spreadsheet_id is None):
        raise ValueError("Must provide either google_spreadsheet_url or google_spreadsheet_id.")

    gsid_pattern = 'https://docs.google.com/spreadsheets/d/(.*)/.*'

    if (google_spreadsheet_id is None) and (google_spreadsheet_url is not None):
        google_spreadsheet_id = re.findall(gsid_pattern, google_spreadsheet_url)[0]

    avdata_url = f"https://docs.google.com/spreadsheets/d/{google_spreadsheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    try:
        df = pd.read_csv(avdata_url)
        return df
    except Exception:
        print(f"Invalid input provided for: url/spreadsheet-id/sheet-name. Check again and then try. \n\tavdata_url: {avdata_url}")

    
df = get_avdata_from_google_spreadsheet(
    google_spreadsheet_id=None, 
    google_spreadsheet_url=GOOGLE_SPREADSHEET_URL,
    sheet_name="AVSources"
).fillna('')

avsources_df = df.drop(columns=["ID"]).rename(columns={
    'Streamlit_Column_Name': 'stcol', 
    'URL': 'url', 
    'Short_Description': 'short_desc', 
    'Long_Description': 'long_desc', 
    'AV_ID': 'av_id'
}).fillna('')

avsources = avsources_df.to_dict(orient='records')

_stcols_names = avsources_df.stcol.unique().tolist()

_stcols_objs = st.beta_columns(len(stcols))
# c1, c2 = st.beta_columns(2)

stcols = dict((k, v) for k, v in zip(_stcols_names, _stcols_objs))
#stcols = dict(c1=c1, c2=c2)

# avsources = [
#     dict(stcol='c1', url="https://youtu.be/CmSKVW1v0xM", short_desc="First URL", long_desc=None, av_id=1), 
#     dict(stcol='c2', url="https://soundcloud.com/imaginedragons/demons", short_desc="Second URL", long_desc=None, av_id=2),
# ]

for idx, avsource in enumerate(avsources):
    with stcols[avsource["stcol"]]:
        url = st.text_input(avsource["short_desc"], avsource["url"])
        event = st_player(url, **options, key=avsource["av_id"])

# with c1:
#     url = st.text_input("First URL", "https://youtu.be/CmSKVW1v0xM")
#     event = st_player(url, **options, key=1)
#     event

# with c2:
#     url = st.text_input("Second URL", "https://soundcloud.com/imaginedragons/demons")
#     event = st_player(url, **options, key=2)
#     event

"---"

with st.beta_expander("Component docstring"):
    st_player

with st.beta_expander("Demo source code"):
    st.code(Path(__file__).read_text())
