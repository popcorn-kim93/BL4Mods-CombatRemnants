# Combat Remnants 0.14.4 설치·사용 안내

전투 후 시체와 소유 관계가 확인된 절단 부위를 한 묶음으로 남깁니다. 데칼과 일반 파티클 잔해는 아직 지원하지 않습니다.

## 설치 및 업데이트

1. Windows x64용 보더랜드 4와 [Borderlands 4 Python SDK](https://bl-sdk.github.io/oak2-mod-db/)가 필요합니다. [호환성 안내](COMPATIBILITY.md)를 확인하세요.
2. 게임을 종료합니다. 네이티브 DLL 교체에는 게임 재시작이 필요합니다.
3. [v0.14.4 릴리즈](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/releases/tag/v0.14.4)에서 **CombatRemnants-0.14.4.zip**을 받습니다. Source code 압축 파일은 설치 파일이 아닙니다.
4. 기존 `sdk_mods/bl4_persistent_effects` 폴더를 `sdk_mods` 밖에 백업한 뒤 새 폴더로 교체합니다. 예전 별도 `bl4_persistence_probe` 폴더도 있다면 밖으로 옮깁니다. 기존 설정인 `sdk_mods/settings/bl4_persistent_effects.json`은 유지합니다. 관리자로 배포한 파일은 해당 관리자를 통해 배포 해제 후 교체하세요.
5. ZIP 안의 `bl4_persistent_effects` 폴더를 게임의 `sdk_mods`에 넣습니다.

```text
Borderlands 4/sdk_mods/bl4_persistent_effects/__init__.py
Borderlands 4/sdk_mods/bl4_persistent_effects/_native/BL4RemovalTrace-abi11.dll
```

6. SDK 메뉴에서 **BL4 Persistent Combat Effects (Experimental)**를 활성화합니다. 현재 게임 안의 Combat Remnants 이름입니다. 플레이어가 준비되면 자동 시작합니다.

최상위 안내 문서와 manifest는 설치할 필요가 없습니다. 수동 설치 기준이며 Vortex 배포는 별도 검증되지 않았습니다.

## 설정

| 옵션 | 기본값과 동작 |
| --- | --- |
| Maximum retained corpses | 50, 범위 0–500. 시체와 연결 부위 전체가 한 묶음이며 오래된 묶음부터 정리 |
| 보스 시체 유지 | 켜짐. 끄면 확인된 Boss. 계열 랭크의 보스와 연결 부위를 보호에서 제외 |
| 원소 사망 처리 | 안 없어지게 / 천천히 사라지게 / 게임 기본 동작. 기본은 천천히 사라지게 |
| 원소 시체 소멸 시간 (초) | 느린 소멸 모드에서 사용. 기본 30초, 범위 1–600초 |

보스 유지 여부를 먼저 판정하고 보호 대상에 원소 정책을 적용합니다. 일반 사망과 연결 파편은 개수 제한까지 유지합니다. 기존 설정 파일이 있으면 새 기본값 대신 저장된 설정을 사용합니다.

설정 개수는 생성량이 아니라 보관 상한입니다. 이미 죽은 NPC와 기존 부위는 소급 수집하지 않습니다. 월드 이동, 강제 파괴, 맵 밖 낙하 등의 정리는 허용합니다. 재접속 후 전장 상태를 복원하지는 않습니다.

## 선택적으로 사용하는 명령

```text
bl4_corpses_status
bl4_corpses_off
bl4_corpses_on --max-corpses 100
```

일반 사용에는 on 명령이 필요 없습니다. `off`는 현재 보호를 중단하고 묶음을 정리합니다. 정리가 끝나면 `on`으로 다시 시작할 수 있습니다. `release_pending`이 true라면 잠시 기다렸다 상태를 확인하세요. 모드 비활성화는 자동 시작도 끕니다. 게임 종료 전 off를 입력할 필요가 없습니다.

`--max-limbs`, `--multiplier`는 이전 호환용이며 무시됩니다. `bl4_effects_on`은 같은 기능의 별칭입니다. 개수 0은 묶음 보호를 해제하며 제어·기록까지 중단하려면 off를 사용합니다.

## 문제 제보

게임 빌드, 옵션, 적 종류와 사망 효과, 화면에서 보인 상태와 해당 세션 보고서를 [Issues](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/issues)에 첨부하세요.

```text
Borderlands 4/sdk_mods/bl4_persistent_effects/reports/
```

시작은 `startup-*.jsonl`, 종료는 `retention-*.native.shutdown.jsonl`과 `*.native.shutdown.native.log`, 일반 추적은 `retention-*.native.jsonl`에 기록됩니다. 공개 전 로그의 로컬 경로를 확인하세요. 게임 업데이트 후 지문 불일치로 시작이 거절되면 검증을 우회하지 말고 오류를 제보하세요.
