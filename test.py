from ytMusicTest import Youtube
from ytmusicapi import setup
from BetterSpotifyTest import Spotify

# setup(filepath="browser.json", headers_raw="""
#     POST /api/stats/qoe?fmt=0&afmt=141&cpn=qXhAGrGxwfrVy_Z2&el=detailpage&ns=yt&fexp=v1%2C24004644%2C494889%2C67154%2C26443548%2C53408%2C34656%2C106030%2C18644%2C14869%2C75925%2C26895%2C9252%2C3479%2C690%2C12340%2C23206%2C7465%2C238%2C7476%2C2%2C27821%2C6374%2C5840%2C11784%2C1548%2C1248%2C13392%2C7087%2C3727%2C591%2C4254%2C1092%2C763%2C2599%2C1725%2C2313%2C1491%2C1592%2C5385%2C3303%2C1091%2C28%2C956%2C8682%2C464%2C270%2C346%2C1445%2C2381%2C103%2C979%2C783%2C131%2C148%2C145%2C848%2C1002%2C858%2C2011%2C5787&cl=777370830&seq=3&docid=kpP4sRFwZbU&ei=CsBqaNOFDv-y0_wPzszBsQs&event=streamingstats&feature=BFa&osid=AAAAAXr_8TQ%3AAOeUNAYEsuCjp7hhuM9xPqszWzTGnaQiFg&plid=AAY5RuDMpMG8UKXO&cbr=Firefox&cbrver=140.0&c=WEB_REMIX&cver=1.20250630.03.00&cplayer=UNIPLAYER&cos=Windows&cosver=10.0&cplatform=DESKTOP&afs=2.497:141::i&ctmp=atrkchg:t.2497;id.und;m.0&cat=hqa&stream=2.612:A&bwm=10.010:475354:0.887&bwe=10.010:302049&cmt=10.010:0.000&bh=10.010:14.662&qclc=ChBxWGhBR3JHeHdmclZ5X1oyEAM HTTP/3
# Host: music.youtube.com
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0
# Accept: */*
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate, br, zstd
# Content-Type: text/plain;charset=UTF-8
# Content-Length: 226
# Referer: https://music.youtube.com/
# X-Goog-Visitor-Id: CgtjelpyMzBPMER3OCiHgKvDBjIKCgJVUxIEGgAgZQ%3D%3D
# X-Goog-AuthUser: 0
# X-YouTube-DataSync-Id: 114425265019751390864||
# Origin: https://music.youtube.com
# Sec-Fetch-Dest: empty
# Sec-Fetch-Mode: cors
# Sec-Fetch-Site: same-origin
# Connection: keep-alive
# Alt-Used: music.youtube.com
# Cookie: __Secure-ROLLOUT_TOKEN=CPCHu6r_n-OXaBDVnIbn7aiOAxiL3_vn7aiOAw%3D%3D; VISITOR_INFO1_LIVE=czZr30O0Dw8; VISITOR_PRIVACY_METADATA=CgJVUxIEGgAgZQ%3D%3D; _gcl_au=1.1.1091866744.1751826380; __Secure-1PSIDTS=sidts-CjIB5H03P9BBg7EHri1ryl9BhzgoLwle0u-ZbkskU9v54nQRHsNTmWoRAV8-eFIK-oDjlxAA; __Secure-3PSIDTS=sidts-CjIB5H03P9BBg7EHri1ryl9BhzgoLwle0u-ZbkskU9v54nQRHsNTmWoRAV8-eFIK-oDjlxAA; HSID=ADuGT__jPvwK9gBwg; SSID=ABxiwKaPZCKMGz1b2; APISID=G8mt6mvGVjxXDDcX/ARUaOYerN3FcLDlPI; SAPISID=-GGLOm5VLg5mgvuC/AnpssdY5zNnH1u_XA; __Secure-1PAPISID=-GGLOm5VLg5mgvuC/AnpssdY5zNnH1u_XA; __Secure-3PAPISID=-GGLOm5VLg5mgvuC/AnpssdY5zNnH1u_XA; SID=g.a000ywhp086dTkZOT9gLhXEa8xHUmZN2g5GGFAXgXvNiIYpKE_azaniloaGUVOnvOaO1VldrmgACgYKAcsSARYSFQHGX2MiMLDFTku91Qg4v9pK_1Uy7RoVAUF8yKrjv1ZF2O1Kl8nsLCcBQuN40076; __Secure-1PSID=g.a000ywhp086dTkZOT9gLhXEa8xHUmZN2g5GGFAXgXvNiIYpKE_azjADh8Z90tXDKf9wbVEU_hgACgYKAYMSARYSFQHGX2MiPi039o_Bzu6OyirS3HxJjRoVAUF8yKoxug4ejU1wrABJJ74aLran0076; __Secure-3PSID=g.a000ywhp086dTkZOT9gLhXEa8xHUmZN2g5GGFAXgXvNiIYpKE_azZlNlVKEZPge9G7dl8ZXOUwACgYKAQsSARYSFQHGX2Mi3oAgeLS5UjryOFg8bHCI0xoVAUF8yKobrBiqhuGl9gQ11sxOlZ5A0076; LOGIN_INFO=AFmmF2swRQIgIwzUQ1LEcdY_1lu5GYlJEeVBK839-yeiwtN9DYUDtqgCIQCWKlZ9FXOx7axRdEBUDIXn5r9f0Hct302vtHtkb-T3ow:QUQ3MjNmd1pMakxlV29xY2VTMWZERFpsSW93RDhqSzRwb2lVWHJSLVAxZDJzdFBRZGRWMmx1eTlNSDlMUTlSWVF6c2RNcXAxYmlndkxNR0hybzRGeW5NTDJMWF9fQVIyaF9sM3B5UTV0b1ZSUElmOHVhZDg1SW53YTNQSGlGQVJZNWdGWkRMMGJaMUJUaXBsOEJCcUFpdjBCamNJZGR0cjRB; YSC=xjYfxMB4SX4; SIDCC=AKEyXzVkpIoPWG1mvvpUNmlSR7lmlPHigN5YosOEy96GUALrap9Gj8k712aiOON79vWJzNFu; __Secure-1PSIDCC=AKEyXzVQkJz245So_o0AI2sd4P1BRoPalw0z3Umfofts4f9F6n9wmgDBP0bPWJxyOMxv35J8; __Secure-3PSIDCC=AKEyXzVH-onrh2nvLmLNNizvEQLearp47eBXEI3U7t4CP6lA3qq8lrseu9YIVk7u1coWhaz5; PREF=repeat=NONE
# Priority: u=4
# TE: trailers
# """)

youtube = Youtube()
spotify = Spotify()

tracks = youtube.get_liked_songs()

uris = spotify.search_songs(tracks)

for i in range(0, len(uris), 100):
    spotify.add_songs_to_playlist(uris[i:i+100], "3PBI6YjES3gjmQhsL1c6go")