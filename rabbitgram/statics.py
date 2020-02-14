SETTINGS_FILE_PATH      = "rabbitgram/settings.yml"

INSTAGRAM_HOMEPAGE      = "https://www.instagram.com/"
INSTAGRAM_LOGIN_URL     = "https://www.instagram.com/accounts/login/ajax/"
INSTAGRAM_USER_PAGE     = "https://www.instagram.com/%s/"

INSTAGRAM_GRAPHQL_URL   = "https://www.instagram.com/graphql/query/"
INSTAGRAM_QUERY_ID      = "e769aa130647d2354c40ea6a439bfc08"
INSTAGRAM_QUERY_URL     = "{}?query_hash={}&variables={{}}".format(INSTAGRAM_GRAPHQL_URL, INSTAGRAM_QUERY_ID)

INSTAGRAM_BASE_HEADERS  = {
    'Accept-Encoding'   : 'gzip, deflate',
    'Accept-Language'   : 'en-US,en;q=0.8',
    'Connection'        : 'keep-alive',
    'Content-Length'    : '0',
    'Host'              : 'www.instagram.com',
    'Origin'            : 'https://www.instagram.com',
    'Referer'           : 'https://www.instagram.com',
    'User-Agent'        : "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
    'X-Instagram-AJAX'  : '1',
    'X-Requested-With'  : 'XMLHttpRequest'
}