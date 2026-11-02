# Combat Remnants 0.11.0 설치·사용 안내

**전투가 끝나도, 흔적은 남는다.**

현재 알파 버전은 적의 시체와 소유 관계가 확인된 절단 부위를 한 묶음으로 유지합니다. 보호 중에는 확인된 시간제 정리·디졸브·몸체 숨김 경로를 막고, 설정한 시체 수를 넘으면 오래된 묶음부터 정리합니다. 혈흔·탄흔·폭발 자국·일반 파티클 잔해는 아직 지원 범위에 포함되지 않습니다.

## 설치

1. Windows x64용 보더랜드 4와 [Borderlands 4 Python SDK](https://bl-sdk.github.io/oak2-mod-db/)가 필요합니다. SDK는 별도로 설치합니다. [호환성 안내](COMPATIBILITY.md)에 기재한 Steam 빌드로 시험했으며 다른 빌드는 확인되지 않았습니다.
2. 게임을 종료합니다. 네이티브 DLL은 게임이 끝날 때까지 메모리에 남으므로 파일 교체 후에는 재시작해야 합니다.
3. [0.11.0 릴리즈](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/releases/tag/v0.11.0)에서 **CombatRemnants-0.11.0.zip**을 받습니다. GitHub가 자동으로 제공하는 **Source code** 압축 파일은 설치 파일이 아닙니다.
4. 이전 시험판을 쓰고 있었다면 `sdk_mods/bl4_persistent_effects` 폴더를 `sdk_mods` 바깥에 백업합니다. 예전 별도 수집기 `bl4_persistence_probe`도 있다면 밖으로 옮깁니다. 수집 기능은 현재 패키지에 통합돼 있습니다. 모드 관리자가 해당 파일을 관리한다면 그 관리자를 통해 기존 배포부터 해제합니다.
5. 압축 안의 **bl4_persistent_effects** 폴더를 게임의 **sdk_mods** 폴더에 넣습니다. 아래와 같이 한 단계만 들어가야 합니다.

   ```text
   Borderlands 4/sdk_mods/bl4_persistent_effects/__init__.py
   Borderlands 4/sdk_mods/bl4_persistent_effects/_native/BL4RemovalTrace-abi9.dll
   ```

6. 게임을 실행하고 SDK 모드 메뉴에서 **BL4 Persistent Combat Effects (Experimental)**를 활성화합니다. 이번 버전은 검증된 실행 파일을 유지하므로 메뉴 표시와 내부 폴더에는 기존 이름을 사용합니다. 이것이 Combat Remnants입니다.

이번 배포는 수동 설치 기준입니다. Vortex 설치 방식은 검증되지 않았습니다. 압축 파일 최상위의 안내 문서와 manifest는 참고용이며 게임 폴더에 넣을 필요가 없습니다.

## 전투 전에 시작

캐릭터로 게임 월드에 들어간 뒤 SDK 콘솔을 열어 입력합니다. 기본 콘솔 키는 보통 `~`이고, 두 번 누르면 확장됩니다. 변경했다면 SDK에 설정한 키를 사용합니다.

```text
bl4_corpses_on --max-corpses 50
```

시체 한 구와 연결된 부위 전체가 한 묶음입니다. 부위 수를 따로 설정하지 않습니다. 50은 기본 설정이며 성능이 검증된 상한이라는 뜻은 아닙니다. 이미 사라진 시체를 복구하는 기능은 아니므로 전투 전에 시작하세요.

**설정한 수는 생성량이 아니라 보관 상한**입니다. 500으로 설정해도 적을 그만큼 처치하지 않았다면 시체 500구가 만들어지지 않습니다. 월드 이동·강제 파괴·맵 밖 낙하 정리는 허용하므로 모든 상황에서 설정 수가 화면에 남는다는 의미도 아닙니다.

실행 중에도 원하는 수로 명령을 다시 입력해 변경할 수 있습니다.

```text
bl4_corpses_on --max-corpses 100
```

메뉴의 **Maximum retained corpses** 설정도 적용됩니다. 개수 없이 `bl4_corpses_on`을 실행하면 메뉴 설정을 사용합니다. 메뉴 범위는 0–500이며, 0은 모든 묶음의 보호를 해제합니다. 제어와 기록을 완전히 종료하려면 아래 `off` 명령을 사용합니다.

기존 `--max-limbs`와 `--multiplier`는 무시됩니다. `bl4_effects_on`은 같은 기능의 별칭이므로 두 명령을 함께 켤 필요가 없습니다. 일반 사용에는 별도의 조사·수집 명령도 필요하지 않습니다.

## 상태 확인·종료

```text
bl4_corpses_status
bl4_corpses_off
```

`status`는 현재 상태를 출력하고 저장합니다. `off`는 연결 부위를 정리하고 시체 정리를 게임에 반환한 뒤 기록을 마칩니다. 정리가 끝난 후 새 세션을 시작하세요. `release_pending`이 true라면 게임을 잠시 유지하고 상태를 다시 확인합니다.

자동 시간 종료는 없습니다. 새 게임 세션에서는 필요할 때 다시 시작합니다. 맵 이동·재접속·저장 파일에 전장의 상태를 보존하는 기능은 아닙니다. 제거할 때는 게임을 종료하고 이 모드의 `bl4_persistent_effects` 폴더만 `sdk_mods` 밖으로 옮깁니다.

## 확인된 범위와 문제 제보

최신 짧은 시험에서는 한도 5구로 76구를 관측했고, 종료 직전 최근 시체 5구와 연결 부위 8개가 남았습니다. 시험자는 화면에서도 시체와 부위가 대체로 함께 남았다고 확인했습니다. 다만 마지막 시체들의 관찰 시간은 약 10–19초였으므로 장시간 방치, 다양한 적·지역, 500구에서의 성능, 멀티플레이는 추가 검증이 필요합니다.

문제가 있으면 **종료 명령을 입력하기 전 화면 상태**를 기록하고 `bl4_corpses_off`로 마칩니다. 아래 폴더의 해당 세션 `retention-*.json`, `retention-*.native.jsonl`과 시작 명령, 게임 빌드, 적 종류·사망 효과를 [Issues](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/issues)에 첨부해 주세요.

```text
Borderlands 4/sdk_mods/bl4_persistent_effects/reports/
```

보고서에는 로컬 모듈 경로 등이 포함될 수 있으므로 공개 전에 내용을 확인하세요. 상세 재질 추적은 기본으로 꺼져 있습니다. 모드가 빌드 검증 실패를 알리면 해당 게임 빌드는 이 패키지의 지원 범위를 벗어난 것입니다. 검증을 우회하지 말고 오류 내용을 알려 주세요.
