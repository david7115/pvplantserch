import streamlit as st
import requests
import pandas as pd
from xml.etree import ElementTree as ET
from urllib.parse import urlparse

# ✅ 인증키 (디코딩된 일반 인증키)
SERVICE_KEY = 'ZarTYb88UP8FCrJp2W+Wxiu4ffdIgJluH8tBA8FKMt553Y+PuBf/2Cxi61wxKU/GfGdeINYC8KuofirJkyf0rA=='
url = 'http://api.data.go.kr/openapi/tn_pubr_public_solar_gen_flct_api'
# ✅ 도메인 검증 함수
def is_valid_domain(url):
    parsed = urlparse(url)
    return parsed.netloc == "api.data.go.kr"

# ✅ XML → pandas 변환 함수
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

# ✅ Streamlit 기본 설정
st.set_page_config(page_title="태양광 발전소 허가정보", layout="wide")
st.title("🔆 전국 태양광 발전소 허가정보 조회 (XML 기반)")

# =========================
# 📥 사용자 입력 - 사이드바
# =========================
with st.sidebar:
    st.header("🔍 조건 입력")
    instt_nm = st.text_input("기관명 (예: 강원특별자치도 동해시)", value="강원특별자치도 동해시")
    page = st.number_input("페이지 번호", min_value=1, value=1)
    num_rows = st.selectbox("페이지당 조회 수", [10, 20, 50, 100], index=3)
    search = st.button("🚀 데이터 조회")

# =========================
# 🚀 API 호출 및 출력
# =========================
if search:
    with st.spinner("📡 공공데이터를 조회 중입니다..."):

        if not is_valid_domain(BASE_URL):
            st.error("❌ 잘못된 API 도메인입니다. 'api.data.go.kr'만 허용됩니다.")
        else:
            params = {
                'serviceKey': SERVICE_KEY,
                'pageNo': page,
                'numOfRows': num_rows,
                'type': 'xml',
                'instt_nm': instt_nm
            }

            try:
                response = requests.get(BASE_URL, params=params, timeout=10)
                response.raise_for_status()

                # XML → pandas DataFrame
                df = parse_xml_to_dataframe(response.content)

                if not df.empty:
                    st.success(f"✅ {len(df)}건의 발전소 정보를 조회했습니다.")
                    st.dataframe(df, use_container_width=True)

                    # 📁 CSV 다운로드
                    csv = df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button("📥 CSV 다운로드", csv, "solar_facility_data.csv", "text/csv")
                else:
                    st.warning("📭 데이터가 없습니다.")

            except ET.ParseError:
                st.error("❗ XML 파싱 오류가 발생했습니다.")
            except requests.exceptions.RequestException as e:
                st.error(f"🚨 API 요청 실패: {e}")
            except Exception as e:
                st.error(f"❗예상치 못한 오류 발생: {e}")
