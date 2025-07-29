import requests

url = 'http://api.data.go.kr/openapi/tn_pubr_public_solar_gen_flct_api'
params ={'serviceKey' : '서비스키', 'pageNo' : '0', 'numOfRows' : '100', 'type' : 'xml', 'SOLAR_GEN_FCLT_NM' : '', 'LCTN_ROAD_NM_ADDR' : '', 'LCTN_LOTNO_ADDR' : '', 'LATITUDE' : '', 'LONGITUDE' : '', 'INSTL_DTL_PSTN_SE_NM' : '', 'OPRTNG_STTS_SE_NM' : '', 'CAPA' : '', 'SPLY_VOLT' : '', 'FREQ' : '', 'INSTL_YR' : '', 'DETLS_USG' : '', 'PRMSN_YMD' : '', 'PRMSN_INST' : '', 'INSTL_AREA' : '', 'CRTR_YMD' : '', 'instt_code' : '4211000', 'instt_nm' : '강원특별자치도 동해시' }

response = requests.get(url, params=params)
print(response.content)
