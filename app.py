import streamlit as st
import requests
import pandas as pd
from urllib.parse import urlparse

# ✅ 인증키 (디코딩된 일반 인증키)
SERVICE_KEY = 'ZarTYb88UP8FCrJp2W+Wxiu4ffdIgJluH8tBA8FKMt553Y+PuBf/2Cxi61wxKU/GfGdeINYC8KuofirJkyf0rA=='

# ✅ 올바른 도메인 (오류 방지를 위해 하드코딩)
BASE_URL = 'https://api.data.go.kr/openapi/tn_pubr_public_solar_gen_flct_api'

# ✅ Streamlit 설정
st.set_page_config(page_title="태양광 발전소 허가정보", layout="wide")
st.title("🔆 전국 태양광 발전소 허가정보 조회 앱")

# =========================
# 📥 사용자 입력 - 사이드바
# =========================
with st.sidebar:
    st.header("🔍 조건 입력")
    instt_nm = st.text_input("기관명 (예: 강원특별자치도 동해시)", value="강원특별자치도 동해시")
    page = st.number_input("페이지 번호", min_value=1, value=1)
    num_rows = st.selectbox("페이지당 조회 수", [10, 20, 50, 100], index=3)
    search = st.button("🚀 조회 실행")

# =========================
# 🔐 도메인 검증 함수
# =========================
def is_valid_domain(url):
    parsed = urlparse(url)
    return parsed.netloc == "api.data.go.kr"

# =========================
# 🚀 API 호출 및 출력
# =========================
if search:
    with st.spinner("📡 공공데이터를 조회 중입니다..."):

        # ✅ 도메인 검증
        if not is_valid_domain(BASE_URL):
            st.error("❌ 잘못된 API 도메인입니다. 'api.data.go.kr'만 허용됩니다.")
        else:
            params = {
                'serviceKey': SERVICE_KEY,
                'pageNo': page,
                'numOfRows': num_rows,
                'type': 'json',
                'instt_nm': instt_nm
            }

            try:
                response = requests.get(BASE_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                header = data.get('response', {}).get('header', {})
                body = data.get('response', {}).get('body', {})
                items = body.get('items', [])

                if header.get('resultCode') == '00' and items:
                    df = pd.DataFrame(items)
                    st.success(f"✅ 총 {body.get('totalCount')}건 중 {len(df)}건을 조회했습니다.")
                    st.dataframe(df, use_container_width=True)

                    # 📥 CSV 다운로드 버튼
                    csv = df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button("📁 CSV 다운로드", csv, "solar_facility_data.csv", "text/csv")

                elif header.get('resultCode') == '03':
                    st.warning("📭 해당 조건에 맞는 데이터가 없습니다.")
                else:
                    st.error(f"⚠️ API 오류: {header.get('resultMsg')}")

            except requests.exceptions.RequestException as e:
                st.error(f"🚨 API 요청 실패: {e}")
            except Exception as e:
                st.error(f"❗예상치 못한 오류 발생: {e}")
