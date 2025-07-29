import streamlit as st
import requests
import pandas as pd

# ✅ 공공데이터포털 디코딩된 인증키
SERVICE_KEY = 'ZarTYb88UP8FCrJp2W+Wxiu4ffdIgJluH8tBA8FKMt553Y+PuBf/2Cxi61wxKU/GfGdeINYC8KuofirJkyf0rA=='
BASE_URL = 'https://api.data.go.kr/openapi/tn_pubr_public_solar_gen_flct_api'

# ✅ Streamlit 기본 설정
st.set_page_config(page_title="태양광 허가정보", layout="wide")
st.title("🔆 전국 태양광 발전소 허가정보 조회")

# =======================
# 📥 사이드바 입력
# =======================
with st.sidebar:
    st.header("🔍 조건 입력")
    instt_nm = st.text_input("기관명 (예: 강원특별자치도 동해시)", value="강원특별자치도 동해시")
    page = st.number_input("페이지 번호", min_value=1, value=1)
    num_rows = st.selectbox("페이지당 조회 수", [10, 20, 50, 100], index=3)
    search = st.button("🚀 조회 실행")

# =======================
# 🚀 API 호출 및 데이터 표시
# =======================
if search:
    with st.spinner("🔄 데이터를 조회 중입니다..."):
        # 요청 파라미터
        params = {
            'serviceKey': SERVICE_KEY,
            'pageNo': page,
            'numOfRows': num_rows,
            'type': 'json',
            'instt_nm': instt_nm
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()  # HTTP 오류 시 예외 발생
            data = response.json()

            header = data.get('response', {}).get('header', {})
            body = data.get('response', {}).get('body', {})
            items = body.get('items', [])

            if header.get('resultCode') == '00' and items:
                df = pd.DataFrame(items)
                st.success(f"✅ 총 {body.get('totalCount')}건 중 {len(df)}건을 조회했습니다.")
                st.dataframe(df, use_container_width=True)

                # 📁 CSV 다운로드 버튼
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 CSV 다운로드",
                    data=csv,
                    file_name="solar_facility_data.csv",
                    mime="text/csv"
                )
            elif header.get('resultCode') == '03':
                st.warning("📭 해당 조건에 맞는 데이터가 없습니다.")
            else:
                st.error(f"⚠️ 오류: {header.get('resultMsg')}")

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 API 요청 실패: {e}")
        except Exception as e:
            st.error(f"❗예상치 못한 오류 발생: {e}")
