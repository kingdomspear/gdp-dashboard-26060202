import streamlit as st
import pandas as pd
import math
from pathlib import Path

st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:',
)

@st.cache_data
def get_gdp_data():
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
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

# -----------------------------------------------------------------------------
# Draw the actual page

'''
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

''
''

min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

countries = gdp_df['Country Code'].unique()

if not len(countries):
    st.warning("Select at least one country")

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'],
    format_func=lambda code: code_to_name.get(code, code),
)

''
''
''

filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries))
    & (gdp_df['Year'] <= to_year)
    & (from_year <= gdp_df['Year'])
]

st.header('GDP over time', divider='gray')

''

st.line_chart(
    filtered_gdp_df,
    x='Year',
    y='GDP',
    color='Country Name',
)

''
''

first_year = gdp_df[gdp_df['Year'] == from_year]
last_year = gdp_df[gdp_df['Year'] == to_year]

st.header(f'GDP in {to_year}', divider='gray')

''

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0]
        last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0]

        if math.isnan(first_gdp):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_gdp / first_gdp:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=code_to_name.get(country, country),
            value=format_gdp(last_gdp),
            delta=growth,
            delta_color=delta_color,
        )
