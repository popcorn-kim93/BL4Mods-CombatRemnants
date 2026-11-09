# GitHub 릴리즈를 Nexus Mods에도 올리기

이 자동화는 GitHub에 공개한 **검증된 릴리즈 ZIP 그대로** Nexus의 기존 파일에 새 버전으로 업로드합니다. 게임이나 모드를 다시 빌드하지 않으며, 개발 소스를 GitHub에 올릴 필요도 없습니다. 알파 릴리즈도 선택적으로 전송할 수 있습니다.

기본 상태는 업로드 비활성화입니다. 설정하지 않은 상태에서는 Nexus에 접속하지 않고 GitHub 파일만 검증합니다. Nexus 페이지를 최초 공개하는 기능은 포함하지 않습니다.

## 한 번만 설정할 항목

1. 이 저장소의 기본 브랜치에 다음 파일을 반영합니다. 이후 새 릴리즈 태그에도 워크플로가 포함되도록 합니다.
   - `.github/workflows/nexus-release.yml`
   - `.github/workflows/nexus-connection.yml`
   - `.github/scripts/nexus_release.py`
   - `NEXUS_RELEASE.ko.md`
   - `.gitignore`의 배포 스크립트 예외 규칙
2. Nexus에 모드 페이지와 최초 파일 하나를 준비합니다. 이 도구는 기존 파일에 버전을 추가하는 방식입니다.
3. Nexus Files의 **Advanced** 또는 **Manage Files** 편집 화면에서 API용 모드 ID와 파일 ID를 확인합니다. 주소창의 숫자나 예전 API의 파일 번호를 대신 넣지 마세요. 공식 업로드 도구가 안내하는 v3 ID를 사용합니다.
4. GitHub 저장소의 **Settings → Secrets and variables → Actions**에 아래 항목을 등록합니다.

| 종류 | 이름 | 값 |
| --- | --- | --- |
| Secret | `NEXUSMODS_API_KEY` | 업로드 권한이 있는 Nexus 계정의 API 키 |
| Variable | `NEXUS_MOD_ID` | 대상 모드의 v3 ID |
| Variable | `NEXUS_FILE_ID` | 버전을 추가할 기존 파일의 v3 ID |
| Variable | `NEXUS_ALLOW_PRERELEASE` | 알파를 포함하려면 `true`. 없거나 다른 값이면 GitHub prerelease를 건너뜀 |
| Variable | `NEXUS_SYNC_ENABLED` | 실제 전송을 시작할 준비가 된 경우에만 `true` |

API 키는 GitHub Secret에 직접 입력합니다. 저장소 파일, 릴리즈 설명, 대화나 로그에 붙여 넣지 않습니다. 현재 공개된 `v0.14.4`는 prerelease이므로 검증하거나 전송하려면 `NEXUS_ALLOW_PRERELEASE=true`가 필요합니다.

바로가기:

- [Nexus API 키 확인·발급](https://www.nexusmods.com/settings/api-keys): 업로드할 모드를 소유하거나 관리하는 계정으로 로그인합니다.
- [GitHub Actions Secrets](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/settings/secrets/actions): **New repository secret**에서 키를 등록합니다.
- [GitHub Actions Variables](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/settings/variables/actions): **New repository variable**에서 대상 ID와 두 설정값을 등록합니다.
- [자동화 실행 화면](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/actions/workflows/nexus-release.yml)

## 먼저 업로드 없이 확인

GitHub **Actions → Mirror release to Nexus Mods → Run workflow**에서 공개된 태그(예: `v0.14.4`)를 입력하고 **dry_run을 켠 채** 실행합니다. 이 실행은 Nexus에 접속하지 않으며 키나 대상 ID도 필요하지 않습니다. 검증 결과와 ZIP 해시는 실행 요약에 표시됩니다.

검증할 파일은 해당 GitHub 릴리즈의 다음 세 가지입니다.

- `CombatRemnants-버전.zip`
- `release-manifest.json`
- `SHA256SUMS.txt`

태그, 제품, 저장소, 버전, 배포 채널, 테스트 빌드 표시, ZIP 전체 해시와 내부 파일 해시를 대조합니다. 누락된 파일, 진단용 채널, 잘못된 경로, 중복 ZIP 항목 등은 거절합니다. 이 검증은 인게임 테스트를 대신하지 않습니다.

API 키와 ID를 입력한 뒤에는 **Actions → Check Nexus connection (read only) → Run workflow**를 실행할 수 있습니다. 이 별도 점검은 저장된 키로 Nexus의 모드 파일 목록과 버전 목록만 조회하여 대상 파일이 해당 모드에 속하는지 확인합니다. 업로드 단계가 없으며 `NEXUS_SYNC_ENABLED=false`에서도 사용할 수 있습니다. 조회 성공은 실제 업로드 권한이나 업로드 완료를 증명하지 않습니다.

## 이후 릴리즈 과정

1. 로컬에서 빌드와 검증을 마치고 공개용 ZIP·manifest·체크섬을 준비합니다.
2. GitHub 릴리즈를 초안으로 만들고 세 파일을 모두 첨부합니다.
3. 첨부가 끝난 뒤 릴리즈를 공개합니다. `published` 이벤트로 자동화가 실행됩니다.
4. 자동화가 같은 ZIP을 내려받아 검증하고, Nexus의 대상 모드와 파일 관계 및 기존 버전을 확인합니다.
5. 설정이 활성화되어 있고 해당 버전이 없으면 공식 Nexus 업로드 도구가 업로드합니다. 반환된 버전 ID가 Nexus 목록에 나타나는지도 확인합니다.

GitHub와 Nexus는 순서대로 처리됩니다. Nexus 업로드가 실패해도 GitHub 릴리즈는 유지됩니다. 기존 릴리즈는 설정만 추가한다고 소급 업로드되지 않습니다. 이미 공개된 버전을 보내려면 수동 실행에서 태그를 지정하고 `dry_run`을 끕니다. 이때도 `NEXUS_SYNC_ENABLED=true`가 필요합니다.

릴리즈를 다른 GitHub Actions 작업에서 생성한다면 이벤트가 실제로 발생하는지 별도 확인하세요. 여기서는 사람이 게시하거나 GitHub CLI로 게시한 릴리즈와 수동 실행을 대상으로 준비했습니다. 외부에서 실행되는 다른 업로드와의 동시 실행은 제어하지 않습니다.

## 바뀌는 항목과 재실행

- Nexus의 기존 파일에 새 버전을 추가하고 모드 버전 표시를 갱신합니다.
- 파일 설명에는 버전, GitHub 릴리즈 링크, 릴리즈 본문을 텍스트로 넣습니다. Markdown을 Nexus 서식으로 변환하지 않습니다.
- 이전 버전을 자동으로 보관 처리하지 않습니다.
- 모드 페이지의 Full description·Short description·이미지·태그와 페이지 공개 상태는 변경하지 않습니다.
- 같은 버전 문자열이 이미 있으면 업로드를 건너뜁니다. 기존 업로드의 내용이 같은지는 별도로 비교하지 않으므로, 잘못된 업로드를 같은 버전으로 덮어쓰는 용도로 사용할 수 없습니다.
- Nexus에 더 높은 숫자 버전이 있으면 이전 버전 업로드를 거절합니다.
- 업로드 도중 실패했다면 Nexus 상태부터 확인한 뒤 재실행합니다. 독립적인 다운로드 해시 검증이나 자동 롤백은 하지 않습니다.

자동화를 중지하려면 `NEXUS_SYNC_ENABLED`를 `false`로 변경합니다. 실행 중인 업로드를 취소하거나 이미 올라간 파일을 삭제하는 설정은 아닙니다.

## 근거와 고정 버전

- [Nexus 공식 업로드 도구 및 ID 확인 안내](https://github.com/Nexus-Mods/upload-action/tree/98532f7670c27cbecc78fae03fa3e278147827e2): 입력 항목, 기존 파일에 버전 추가, API v3 사용 방식을 확인했습니다.
- 업로드 도구는 `98532f7670c27cbecc78fae03fa3e278147827e2`에 고정합니다. 사전 조회는 같은 리비전의 `src/openapi.schema.ts`를 기준으로 작성했습니다.
- checkout은 `11d5960a326750d5838078e36cf38b85af677262`에 고정합니다.
- 현재 로컬 검사는 파일 검증·대상 검사·업로드 조건을 대상으로 합니다. 실제 Nexus 인증, 권한, 업로드와 GitHub Actions 실행 성공은 연결 후 별도로 확인해야 합니다.
