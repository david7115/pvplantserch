import streamlit as st
import requests
import pandas as pd

# ✅ API 인증키 (공공데이터포털 디코딩된 키)
SERVICE_KEY = 'ZarTYb88UP8FCrJp2W%2BWxiu4ffdIgJluH8tBA8FKMt553Y%2BPuBf%2F2Cxi61wxKU%2FGfGdeINYC8KuofirJkyf0rA%3D%3D'
BASE_URL = 'http://api.data.go.kr/openapi/tn_pubr_public_solar_gen_flct_api'

# ✅ 시군구별 샘플 기관
CITY_CODE_MAP = {
    "강원특별자치도 동해시": "4211000",
    "경기도 안성시": "4155000",
    "전라북도 전주시": "4511000",
    "충청남도 당진시": "4427000",
    "제주특별자치도 서귀포시": "5013000"
}

# ✅ Streamlit 설정
st.set_page_config(page_title="태양광 허가정보", layout="wide")
st.title("🔆 전국 태양광 발전소 허가정보 조회")

# ✅ 사이드바 UI
with st.sidebar:
    st.header("🔍 조건 입력")
    city = st.selectbox("기관명 선택", list(CITY_CODE_MAP.keys()))
    page = st.number_input("페이지 번호", min_value=1, value=1)
    num_rows = st.selectbox("페이지당 조회 수", [10, 20, 50, 100], index=3)
    search = st.button("🚀 데이터 조회")

# ✅ 조회 실행
if search:
    with st.spinner("📡 데이터를 조회 중입니다..."):
        instt_code = CITY_CODE_MAP[city]

        params = {
            'serviceKey': SERVICE_KEY,
            'pageNo': page,
            'numOfRows': num_rows,
            'type': 'json',
            'instt_nm': city,
            'instt_code': instt_code
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            header = data.get('response', {}).get('header', {})
            items = data.get('response', {}).get('body', {}).get('items', [])

            if header.get('resultCode') == '00' and items:
                df = pd.DataFrame(items)
                st.success(f"✅ {len(df)}건 조회 완료")
                st.dataframe(df, use_container_width=True)

                # CSV 다운로드
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 CSV 다운로드", csv, "solar_facilities.csv", "text/csv")
            elif header.get('resultCode') == '03':
                st.warning("📭 조건에 맞는 데이터가 없습니다.")
            else:
                st.error(f"⚠️ API 오류: {header.get('resultMsg')}")

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 API 요청 실패: {e}")
