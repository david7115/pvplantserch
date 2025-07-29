import requests

# ✅ API 요청 URL (https로 수정)
url = 'https://api.data.go.kr/openapi/tn_pubr_public_solar_gen_flct_api'

# ✅ 디코딩된 서비스 키
service_key = 'ZarTYb88UP8FCrJp2W+Wxiu4ffdIgJluH8tBA8FKMt553Y+PuBf/2Cxi61wxKU/GfGdeINYC8KuofirJkyf0rA=='

# ✅ 요청 파라미터
params = {
    'serviceKey': service_key,
    'pageNo': '1',
    'numOfRows': '100',
    'type': 'xml',  # 또는 'json'으로 변경 가능
    'SOLAR_GEN_FCLT_NM': '',
    'LCTN_ROAD_NM_ADDR': '',
    'LCTN_LOTNO_ADDR': '',
    'LATITUDE': '',
    'LONGITUDE': '',
    'INSTL_DTL_PSTN_SE_NM': '',
    'OPRTNG_STTS_SE_NM': '',
    'CAPA': '',
    'SPLY_VOLT': '',
    'FREQ': '',
    'INSTL_YR': '',
    'DETLS_USG': '',
    'PRMSN_YMD': '',
    'PRMSN_INST': '',
    'INSTL_AREA': '',
    'CRTR_YMD': '',
    'instt_code': '4211000',                # 동해시 코드
    'instt_nm': '강원특별자치도 동해시'      # 기관명
}

# ✅ API 요청 실행
response = requests.get(url, params=params)

# ✅ 결과 출력 (raw XML)
print(response.content.decode('utf-8'))
