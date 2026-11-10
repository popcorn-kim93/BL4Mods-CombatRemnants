# Combat Remnants 0.18.3 설치·사용 안내

시체와 연결 절단 부위, 확인된 탄흔·핏자국·폭발 자국을 남깁니다. 일반 파티클 잔해는 아직 지원하지 않습니다.

## 설치 및 업데이트

1. Windows x64용 보더랜드 4와 [Borderlands 4 Python SDK](https://bl-sdk.github.io/oak2-mod-db/)가 필요합니다. [호환성](COMPATIBILITY.md)을 확인하세요.
2. 게임을 완전히 종료합니다. DLL과 이미 불러온 Python 코드는 새 게임 프로세스에서 적용됩니다.
3. [Releases](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/releases)의 **CombatRemnants-0.18.3.zip**을 받습니다. Source code 압축 파일은 설치 파일이 아닙니다.
4. 기존 `sdk_mods/bl4_persistent_effects` 폴더를 `sdk_mods` 밖에 백업한 뒤 교체합니다. 예전 별도 `bl4_persistence_probe` 폴더도 밖으로 옮깁니다. 기존 `sdk_mods/settings/bl4_persistent_effects.json`은 보존하세요. 모드 관리자가 배포한 파일은 해당 관리자로 배포 해제 후 수동 교체하세요.
5. ZIP 안의 `bl4_persistent_effects` 폴더를 게임의 `sdk_mods` 바로 아래에 넣습니다.

```text
Borderlands 4/sdk_mods/bl4_persistent_effects/__init__.py
Borderlands 4/sdk_mods/bl4_persistent_effects/_native/BL4RemovalTrace-abi12.dll
```

6. 설정 파일이 없는 최초 설치는 **BL4 Persistent Combat Effects (Experimental)**가 자동 활성화됩니다. 기존에 꺼 둔 상태는 유지하므로 그 경우 SDK 메뉴에서 켜 주세요. 현재 게임 안의 Combat Remnants 이름입니다. 플레이어가 준비되면 자동 시작하며, 월드 안에서 켜도 별도 on 명령이 필요 없습니다.

최상위 문서는 설치하지 않아도 됩니다. 수동 설치 기준이며 Vortex 배포는 별도 검증되지 않았습니다.

## 언어와 설정

언어 기본값은 **Auto / 자동**입니다. 게임이 한국어이면 한국어, 그 외에는 영어로 표시합니다. **한국어 / English**를 직접 선택한 뒤 설정 메뉴를 다시 열면 수동으로 바꿀 수 있습니다. 게임 언어 자체는 변경하지 않습니다. 명령어와 진단 JSON의 필드 이름은 번역하지 않고 유지합니다.

| 옵션 | 기본값과 동작 |
| --- | --- |
| 최대 유지 시체 수 | 50, 범위 0–500. 시체와 연결 부위 전체가 한 묶음 |
| 보스 시체 유지 | 켜짐. Boss 및 Boss.* 등급을 원소 사망 정책보다 먼저 판정 |
| 원소 사망 처리 | 천천히 사라지게. 무기한 유지 / 게임 기본 동작도 선택 가능 |
| 원소 시체 소멸 시간 | 30초, 범위 1–600초. 느린 소멸 모드에서 사용 |
| 전투 데칼 유지 | 켜짐. 확인된 탄흔·핏자국·폭발 자국만 관리 |
| 탄흔 / 핏자국 / 폭발 자국 최대 개수 | 512 / 128 / 64개, 각각 0–4096개 |
| 탄흔 / 핏자국 / 폭발 자국 지속시간 | 모두 0초(무한), 각각 0–3600초 |

기존 저장값이 있으면 기본값보다 우선합니다. 데칼 한도에 도달하면 같은 종류의 가장 오래된 자국을 새 자국으로 교체하며 다른 종류의 한도를 사용하지 않습니다. **개수 0**은 그 종류의 보관 원본을 정리하고 새 자국을 게임에 맡기는 설정입니다. **시간 0**은 시간제한만 없애며 개수 제한은 유지합니다. 유한한 시간은 마지막 1초 동안 흐려지며 새 자국부터 적용됩니다. 개수 한도를 줄이면 초과하는 오래된 항목을 정리합니다.

피해 영역·웅덩이·경고 표시·미확인 재질은 유지 대상이 아닙니다. 게임이 원래 데칼을 받지 않게 설정한 메시에는 강제로 생성하지 않습니다. 이미 죽은 NPC와 기존 부위는 소급 수집하지 않습니다. 다른 월드로 바뀌면 데칼 목록을 정리하며, 같은 월드 안의 빠른 이동은 목록이 유지될 수 있습니다. 재접속 후 전장 상태를 복원하지 않습니다.

## 선택 명령과 문제 제보

```text
bl4_corpses_status
bl4_decals_status
bl4_corpses_off
bl4_corpses_on --max-corpses 100
bl4_decals_off
bl4_decals_on
```

corpses off는 데칼을 포함한 유지 세션을 중단합니다. decals off는 데칼 유지 기능만 끕니다. 모드 비활성화는 자동 시작도 끕니다. 게임 종료 전에 off를 입력할 필요는 없습니다. 지속적으로 사용할 설정은 메뉴에서 변경하세요.

분석이 필요할 때만 `bl4_decals_start` → 문제 재현 → `bl4_decals_stop`으로 짧게 수집하세요. **start/stop은 진단 수집 명령이며 유지 기능을 켜고 끄는 명령이 아닙니다.** 상세 추적은 용량과 실행 비용이 크므로 평상시 플레이에는 필요하지 않습니다.

게임 빌드, 실제 설정값, 화면에서 보인 상태, `sdk_mods/bl4_persistent_effects/reports`의 해당 `decal-events-*.summary.json`을 [Issues](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/issues)에 첨부하세요. 상세 JSONL도 보관하되 공개 전 로컬 경로를 확인하세요.
