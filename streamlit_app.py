import streamlit as st
import pandas as pd
import math
import json
from pathlib import Path

st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:',
    layout='wide',
)

# -----------------------------------------------------------------------------
# Global styles

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;400;500;700&display=swap');

/* ── Base ── */
html, body, .stApp {
    background: #FAF7F2 !important;
    font-family: 'Noto Serif KR', 'Malgun Gothic', Georgia, serif !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #F0EAE0 !important;
    border-right: 1px solid rgba(195, 178, 155, 0.22) !important;
}
section[data-testid="stSidebar"] * {
    font-family: 'Noto Serif KR', serif !important;
}
section[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255, 252, 248, 0.85) !important;
    border: 1px solid rgba(175, 155, 130, 0.3) !important;
    border-radius: 10px !important;
    color: #3D3630 !important;
}
section[data-testid="stSidebar"] .stCaption {
    color: #9A8C82 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.02em !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid rgba(195, 178, 155, 0.25) !important;
    gap: 4px !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Noto Serif KR', serif !important;
    color: #9A8C82 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.04em !important;
    padding: 8px 20px !important;
    border-radius: 8px 8px 0 0 !important;
    transition: color 0.2s ease !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #3D3630 !important;
    background: rgba(255, 252, 248, 0.6) !important;
    border-bottom: 2px solid #9DAE9B !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: rgba(255, 252, 248, 0.92) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(195, 178, 155, 0.18) !important;
    padding: 18px 22px !important;
    margin: 10px 0 !important;
    box-shadow: 0 2px 20px rgba(110, 92, 75, 0.07) !important;
    transition: box-shadow 0.3s ease !important;
}
[data-testid="stChatMessage"]:hover {
    box-shadow: 0 4px 28px rgba(110, 92, 75, 0.11) !important;
}
[data-testid="stChatMessageContent"],
[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] li {
    font-family: 'Noto Serif KR', serif !important;
    color: #3D3630 !important;
    line-height: 1.95 !important;
    letter-spacing: 0.025em !important;
    font-size: 0.94rem !important;
}
[data-testid="stChatMessageContent"] strong {
    color: #5A4D42 !important;
    font-weight: 600 !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    border-radius: 30px !important;
    background: rgba(255, 252, 248, 0.96) !important;
    border: 1.5px solid rgba(175, 155, 130, 0.3) !important;
    box-shadow: 0 2px 16px rgba(110, 92, 75, 0.07) !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #B5C4B1 !important;
    box-shadow: 0 3px 22px rgba(110, 92, 75, 0.13) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Noto Serif KR', serif !important;
    color: #3D3630 !important;
    background: transparent !important;
    font-size: 0.93rem !important;
    letter-spacing: 0.02em !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #BFB2A4 !important;
    font-style: italic !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] label {
    font-family: 'Noto Serif KR', serif !important;
    color: #6B5F55 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.04em !important;
}
[data-testid="stSelectbox"] > div > div {
    background: rgba(255, 252, 248, 0.95) !important;
    border: 1.5px solid rgba(175, 155, 130, 0.28) !important;
    border-radius: 12px !important;
    color: #3D3630 !important;
    font-family: 'Noto Serif KR', serif !important;
    box-shadow: 0 2px 12px rgba(110, 92, 75, 0.05) !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
    font-family: 'Noto Serif KR', serif !important;
    border-radius: 22px !important;
    color: #8A7B6E !important;
    border: 1px solid rgba(175, 155, 130, 0.32) !important;
    background: transparent !important;
    font-size: 0.84rem !important;
    letter-spacing: 0.04em !important;
    transition: all 0.22s ease !important;
    padding: 0.3rem 1.1rem !important;
}
[data-testid="stButton"] > button:hover {
    background: rgba(175, 155, 130, 0.1) !important;
    border-color: rgba(175, 155, 130, 0.5) !important;
    color: #5A4D42 !important;
    box-shadow: 0 2px 10px rgba(110, 92, 75, 0.08) !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(195, 178, 155, 0.25) !important;
    margin: 1.6rem 0 !important;
}

/* ── Alert/Info box ── */
[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: 1px solid rgba(195, 178, 155, 0.2) !important;
    background: rgba(255, 252, 248, 0.85) !important;
    font-family: 'Noto Serif KR', serif !important;
}
[data-testid="stAlert"] p {
    color: #6B5F55 !important;
    font-size: 0.91rem !important;
    letter-spacing: 0.02em !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: rgba(245, 240, 232, 0.4); }
::-webkit-scrollbar-thumb { background: rgba(175, 155, 130, 0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(175, 155, 130, 0.5); }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Data & helpers

@st.cache_data
def get_gdp_data():
    DATA_FILENAME = Path(__file__).parent / 'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)
    MIN_YEAR = 1960
    MAX_YEAR = 2022
    gdp_df = raw_gdp_df.melt(
        ['Country Code', 'Country Name'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
    return gdp_df


gdp_df = get_gdp_data()

code_to_name = (
    gdp_df[['Country Code', 'Country Name']]
    .drop_duplicates()
    .set_index('Country Code')['Country Name']
    .to_dict()
)


def format_gdp(value_usd):
    if math.isnan(value_usd):
        return 'n/a'
    if abs(value_usd) >= 1e12:
        return f'{value_usd / 1e12:,.2f}T'
    elif abs(value_usd) >= 1e9:
        return f'{value_usd / 1e9:,.2f}B'
    elif abs(value_usd) >= 1e6:
        return f'{value_usd / 1e6:,.2f}M'
    else:
        return f'{value_usd / 1e3:,.2f}K'


def get_travel_recommendations(region: str, api_key: str) -> dict:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'system',
                'content': (
                    '당신은 여행 전문가입니다. 사용자가 지역명을 입력하면 그 지역의 인기 여행지 5~7곳을 추천해 주세요.\n'
                    '반드시 아래 JSON 형식으로만 응답하세요:\n'
                    '{\n'
                    '  "region": "지역명",\n'
                    '  "intro": "지역 소개 한 문장",\n'
                    '  "destinations": [\n'
                    '    {"name": "장소명", "description": "간단한 설명 (한국어, 1~2문장)", "lat": 위도, "lon": 경도},\n'
                    '    ...\n'
                    '  ]\n'
                    '}\n'
                    '좌표는 반드시 정확한 실제 좌표를 사용하세요.'
                ),
            },
            {'role': 'user', 'content': f'{region} 지역의 인기 여행지를 추천해 주세요.'},
        ],
        response_format={'type': 'json_object'},
    )
    return json.loads(response.choices[0].message.content)


# -----------------------------------------------------------------------------
# Sidebar

with st.sidebar:
    st.header('설정')

    with st.expander('🔑 OpenAI API Key', expanded=True):
        st.text_input(
            'API Key',
            type='password',
            placeholder='sk-...',
            key='openai_api_key',
            label_visibility='collapsed',
            help='입력 후 Enter를 누르거나 다른 곳을 클릭하면 저장됩니다.',
        )
        if st.session_state.get('openai_api_key'):
            st.caption('✅ API Key가 등록되어 있습니다.')
        else:
            st.caption('❌ API Key가 등록되지 않았습니다.')

    st.divider()

    st.header('필터')

    min_value = gdp_df['Year'].min()
    max_value = gdp_df['Year'].max()

    from_year, to_year = st.slider(
        '조회 기간',
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value],
    )

    countries = gdp_df['Country Code'].unique()

    selected_countries = st.multiselect(
        '국가 선택',
        countries,
        ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'],
        format_func=lambda code: code_to_name.get(code, code),
    )

    if not selected_countries:
        st.warning('국가를 하나 이상 선택하세요.')


# -----------------------------------------------------------------------------
# Tabs

tab_gdp, tab_travel = st.tabs(['📊 GDP 대시보드', '✈️ 여행지 추천'])

# ── Tab 1: GDP Dashboard ──────────────────────────────────────────────────────

with tab_gdp:
    '''
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
    '''

    ''
    ''

    filtered_gdp_df = gdp_df[
        (gdp_df['Country Code'].isin(selected_countries))
        & (gdp_df['Year'] <= to_year)
        & (from_year <= gdp_df['Year'])
    ]

    st.header('GDP over time', divider='gray')
    ''

    if selected_countries:
        st.line_chart(filtered_gdp_df, x='Year', y='GDP', color='Country Name')

    ''
    ''

    first_year = gdp_df[gdp_df['Year'] == from_year]
    last_year  = gdp_df[gdp_df['Year'] == to_year]

    st.header(f'GDP in {to_year}', divider='gray')
    ''

    if selected_countries:
        cols = st.columns(4)
        for i, country in enumerate(selected_countries):
            col = cols[i % len(cols)]
            with col:
                first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0]
                last_gdp  = last_year[last_year['Country Code'] == country]['GDP'].iat[0]

                if math.isnan(first_gdp):
                    growth, delta_color = 'n/a', 'off'
                else:
                    growth, delta_color = f'{last_gdp / first_gdp:,.2f}x', 'normal'

                st.metric(
                    label=code_to_name.get(country, country),
                    value=format_gdp(last_gdp),
                    delta=growth,
                    delta_color=delta_color,
                )

# ── Tab 2: Travel Chatbot ─────────────────────────────────────────────────────

with tab_travel:

    # ── Hero header ──────────────────────────────────────────────────────────
    st.html("""
    <div style="
        text-align: center;
        padding: 52px 40px 44px;
        background: linear-gradient(150deg, #EDE5D8 0%, #E4D9C8 45%, #D9CCBA 100%);
        border-radius: 24px;
        margin-bottom: 32px;
        border: 1px solid rgba(195, 178, 155, 0.2);
        box-shadow: 0 6px 40px rgba(110, 90, 70, 0.08);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute; top: 18px; left: 28px;
            font-size: 0.85rem; opacity: 0.22; letter-spacing: 10px; color: #7A6A58;
        ">✦ &nbsp; ✦ &nbsp; ✦</div>
        <div style="
            position: absolute; bottom: 18px; right: 28px;
            font-size: 0.85rem; opacity: 0.22; letter-spacing: 10px; color: #7A6A58;
        ">✦ &nbsp; ✦ &nbsp; ✦</div>

        <div style="font-size: 3rem; margin-bottom: 14px;">🌿</div>
        <h1 style="
            font-family: 'Noto Serif KR', serif;
            color: #3D3630;
            font-weight: 500;
            font-size: 1.75rem;
            letter-spacing: 0.15em;
            margin: 0 0 14px;
            line-height: 1.3;
        ">여 행 지 추 천</h1>
        <div style="
            width: 48px; height: 1px;
            background: rgba(145, 125, 100, 0.45);
            margin: 0 auto 16px;
        "></div>
        <p style="
            font-family: 'Noto Serif KR', serif;
            color: #8C7D6E;
            font-size: 0.88rem;
            letter-spacing: 0.1em;
            margin: 0;
            font-weight: 300;
            line-height: 2;
        ">가고 싶은 지역을 알려주세요<br>당신만의 여행 이야기를 시작해 드릴게요</p>
    </div>
    """)

    if not st.session_state.get('openai_api_key'):
        st.html("""
        <div style="
            text-align: center;
            padding: 28px 32px;
            background: rgba(255, 252, 248, 0.88);
            border-radius: 16px;
            border: 1px solid rgba(195, 178, 155, 0.2);
            color: #8C7D6E;
            font-family: 'Noto Serif KR', serif;
            font-size: 0.9rem;
            letter-spacing: 0.04em;
            line-height: 1.9;
        ">
            🔑 &nbsp; 왼쪽 사이드바의 설정에서<br>
            <strong style="color: #5A4D42;">OpenAI API Key</strong>를 먼저 등록해 주세요.
        </div>
        """)
    else:
        if 'travel_messages' not in st.session_state:
            st.session_state.travel_messages = []
        if 'travel_destinations' not in st.session_state:
            st.session_state.travel_destinations = None

        # Reset button (right-aligned)
        _, btn_col = st.columns([6, 1])
        with btn_col:
            if st.button('초기화'):
                st.session_state.travel_messages = []
                st.session_state.travel_destinations = None
                st.rerun()

        # Chat history
        for msg in st.session_state.travel_messages:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])

        # Destination selector + map
        if st.session_state.travel_destinations:
            destinations = st.session_state.travel_destinations
            dest_options = {d['name']: d for d in destinations}

            st.html('<div style="margin-top: 8px;"></div>')
            st.divider()

            # Map section header
            st.html("""
            <p style="
                font-family: 'Noto Serif KR', serif;
                color: #8C7D6E;
                font-size: 0.84rem;
                letter-spacing: 0.08em;
                margin: 0 0 6px;
                font-weight: 300;
            ">✦ &nbsp; 여행지를 선택하면 지도를 볼 수 있습니다</p>
            """)

            selected_name = st.selectbox(
                '여행지 선택',
                list(dest_options.keys()),
                label_visibility='collapsed',
            )

            if selected_name:
                import folium
                from streamlit_folium import st_folium

                sel = dest_options[selected_name]

                # Map description card
                st.html(f"""
                <div style="
                    padding: 16px 22px;
                    background: rgba(255, 252, 248, 0.9);
                    border-radius: 14px;
                    border: 1px solid rgba(195, 178, 155, 0.18);
                    box-shadow: 0 2px 16px rgba(110, 92, 75, 0.06);
                    margin: 12px 0 16px;
                ">
                    <p style="
                        font-family: 'Noto Serif KR', serif;
                        color: #3D3630;
                        font-size: 1.05rem;
                        font-weight: 500;
                        letter-spacing: 0.06em;
                        margin: 0 0 6px;
                    ">{sel['name']}</p>
                    <p style="
                        font-family: 'Noto Serif KR', serif;
                        color: #9A8C82;
                        font-size: 0.87rem;
                        letter-spacing: 0.03em;
                        line-height: 1.7;
                        margin: 0;
                        font-weight: 300;
                    ">{sel['description']}</p>
                </div>
                """)

                m = folium.Map(
                    location=[sel['lat'], sel['lon']],
                    zoom_start=14,
                    tiles='CartoDB positron',
                )
                folium.Marker(
                    [sel['lat'], sel['lon']],
                    popup=folium.Popup(
                        f"<b style='font-family:serif'>{sel['name']}</b>",
                        max_width=200,
                    ),
                    tooltip=sel['name'],
                    icon=folium.Icon(color='darkgreen', icon='leaf', prefix='fa'),
                ).add_to(m)
                st_folium(m, width=700, height=420)

        # Chat input
        if prompt := st.chat_input('지역명을 입력하세요  (예: 제주도, 파리, 도쿄)'):
            st.session_state.travel_messages.append({'role': 'user', 'content': prompt})

            with st.chat_message('user'):
                st.markdown(prompt)

            with st.chat_message('assistant'):
                with st.spinner(''):
                    try:
                        result = get_travel_recommendations(
                            prompt, st.session_state['openai_api_key']
                        )
                        destinations = result.get('destinations', [])
                        st.session_state.travel_destinations = destinations

                        dest_list = '\n\n'.join(
                            f"**{i + 1}. {d['name']}** — {d['description']}"
                            for i, d in enumerate(destinations)
                        )
                        reply = (
                            f"**{result.get('region', prompt)}** 인기 여행지를 소개합니다.\n\n"
                            f"*{result.get('intro', '')}*\n\n"
                            f"{dest_list}\n\n"
                            f"아래 목록에서 여행지를 선택하면 지도를 볼 수 있습니다."
                        )
                        st.markdown(reply)
                        st.session_state.travel_messages.append(
                            {'role': 'assistant', 'content': reply}
                        )

                    except Exception as e:
                        err = f"오류가 발생했습니다: {e}"
                        st.error(err)
                        st.session_state.travel_messages.append(
                            {'role': 'assistant', 'content': err}
                        )

            st.rerun()
