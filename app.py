import streamlit as st
import requests
import pandas as pd
from xml.etree import ElementTree as ET
from urllib.parse import urlparse

# ✅ API 인증키 및 기본 URL
SERVICE_KEY = 'ZarTYb88UP8FCrJp2W+Wxiu4ffdIgJluH8tBA8FKMt553Y+PuBf/2Cxi61wxKU/GfGdeINYC8KuofirJkyf0rA=='
BASE_URL = 'https://api.data.go.kr/openapi/tn_pubr_public_solar_gen_flct_api'

# ✅ 시군구별 샘플 코드 (확장 가능)
CITY_CODE_MAP = {
    "강원특별자치도 동해시": "4211000",
    "경기도 안성시": "4155000",
    "전라북도 전주시": "4511000",
    "충청남도 당진시": "4427000",
    "제주특별자치도 서귀포시": "5013000"
}

# ✅ 도메인 확인 함수
def is_valid_domain(url):
    parsed = urlparse(url)
    return parsed.netloc == "api.data.go.kr"

# ✅ XML → DataFrame 파싱 함수
def parse_xml_to_dataframe(xml_data):
    root = ET.fromstring(xml_data)
    items = root.findall(".//item")

    data = []
    for item in items:
        row = {
            '발전소명': item.findtext('SOLAR_GEN_FCLT_NM'),
            '주소': item.findtext('LCTN_ROAD_NM_ADDR') or item.findtext('LCTN_LOTNO_ADDR'),
            '설비용량(kW)': item.findtext('CAPA'),
            '허가일': item.findtext('PRMSN_YMD'),
            '운영상태': item.findtext('OPRTNG_STTS_SE_NM'),
            '위도': item.findtext('LATITUDE'),
            '경도': item.findtext('LONGITUDE'),
        }
        data.append(row)

    return pd.DataFrame(data)

# ✅ Streamlit UI 설정
st.set_page_config(page_title="태양광 발전소 허가정보", layout="wide")
st.title("🌞 전국 태양광 발전소 허가정보 조회 (행정기관 코드 연동)")

# ✅ 사이드바 입력 UI
with st.sidebar:
    st.header("🔍 조건 입력")
    city = st.selectbox("기관명 선택", list(CITY_CODE_MAP.keys()))
    page = st.number_input("페이지 번호", min_value=1, value=1)
    num_rows = st.selectbox("페이지당 조회 수", [10, 20, 50, 100], index=3)
    query = st.button("🚀 데이터 조회")

# ✅ 조회 실행
if query:
    with st.spinner("📡 데이터를 조회 중입니다..."):

        if not is_valid_domain(BASE_URL):
            st.error("❌ API 도메인이 잘못되었습니다.")
        else:
            # ✅ 선택된 기관명과 코드
            instt_nm = city
            instt_code = CITY_CODE_MAP[city]

            params = {
                'serviceKey': SERVICE_KEY,
                'pageNo': page,
                'numOfRows': num_rows,
                'type': 'xml',
                'instt_nm': instt_nm,
                'instt_code': instt_code
            }

            try:
                response = requests.get(BASE_URL, params=params, timeout=10)
                response.raise_for_status()

                df = parse_xml_to_dataframe(response.content)

                if not df.empty:
                    st.success(f"✅ 총 {len(df)}건의 발전소 정보를 조회했습니다.")
                    st.dataframe(df, use_container_width=True)

                    csv = df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button("📥 CSV 다운로드", csv, "solar_data.csv", "text/csv")
                else:
                    st.warning("📭 조회 조건에 해당하는 데이터가 없습니다. 다른 기관을 선택해보세요.")

            except ET.ParseError:
                st.error("❗ XML 파싱 오류 발생")
            except requests.exceptions.RequestException as e:
                st.error(f"🚨 API 요청 실패: {e}")
            except Exception as e:
                st.error(f"❗예상치 못한 오류 발생: {e}")
