# BITA Peucedanum HA site-recovery inquiry packet v1

## Purpose

The remaining bottleneck for the Taisetsu `Peucedanum multivittatum` technical pilot is no longer biological design. It is exact-site and authorization recovery.

Primary papers identify the Taisetsu study region only broadly (`43°32–33'N, 142°51–53'E`) and use plot codes such as HA and HL. Current National Park zoning and permit routing cannot be closed reliably from those broad coordinates.

The corresponding author of the 2021 and 2025 studies is Prof./Assoc. Prof. Gaku Kudo, Faculty of Environmental Earth Science, Hokkaido University. The published correspondence address is:

```text
gaku@ees.hokudai.ac.jp
```

Do not send this inquiry automatically. It is a ready-to-review contact packet.

## Information to recover from the original field programme

Ask for the following factual items together, because they determine both ecological feasibility and current permit routing:

1. exact or operationally sufficient coordinates of plot HA,
2. municipality / local place name,
3. whether HA is inside Daisetsuzan National Park and, if known, the park-zone class,
4. site/land manager used for the 2021 and later experiments,
5. what authorization was used for flower/plant handling at HA,
6. what authorization was used for predator-egg removal,
7. what authorization was used for leaf sampling/genotyping,
8. whether the 7 m x 7 m HA plot is still identifiable/reusable or whether the exact location is sensitive,
9. practical access constraints and preferred approach route,
10. whether a new manipulation study should be coordinated with the existing long-term field programme rather than independently relocating the site.

The historical authorization information is a routing clue only; current project permission must still be obtained separately.

## Draft inquiry to the original field investigator

### Suggested subject

```text
大雪山ハクサンボウフウ HA 調査地・許可手続きについてのご相談
```

### Draft body

```text
工藤 岳 先生

突然のご連絡失礼いたします。

ハクサンボウフウ（Peucedanum multivittatum）の雄花・両性花の機能分化と種子捕食の関係について、先生方の2021年 Ecology and Evolution 論文および2025年 Journal of Ecology 論文を拝読し、追試・発展実験の可能性を検討しております。

現在考えているのは、まず小規模な技術試験として、終散形花序の共通雄期が終了した後に両性花／雄花を判別し、総花数をそろえたまま両性花割合を操作できるかを検証するものです。本試験に進む場合には、先生方が行われた産卵数の記録・孵化前の卵除去・結実追跡を組み合わせることを想定しています。

ただし、新規の現地操作を計画する前に、既存調査地と許可手続きを正確に確認すべきと考えております。差し支えない範囲で、以下についてご教示いただくことは可能でしょうか。

1. 論文中の HA 調査区の正確な位置、または許可申請・現地確認に十分な位置情報
2. HA の所在自治体・地名、および国立公園内の地種区分をご存じでしたらその区分
3. 2021年の106個体調査で、捕食者卵の除去、葉採取、個体標識等に用いられた許可・届出の種類と窓口
4. 現在も同一地点で調査を継続されているか、また新しい操作実験を行う場合に既存調査との調整が必要か
5. 調査地情報の取り扱いに機微性がある場合、どの程度の情報共有が適切か

なお、環境省の2025年7月改定の大雪山国立公園指定植物リストでは、ハクサンボウフウが指定植物として掲載されていることを確認しています。そのため、花の除去操作や葉採取については、新規計画として改めて必要な許可を確認する前提です。

先生方の既存調査に支障を与えないことを最優先に検討したく、もしこの系での操作実験自体が現実的でない、あるいは別地点の方が適切というご判断がありましたら、その点もご教示いただけますと大変助かります。

どうぞよろしくお願いいたします。
```

## Follow-up inquiry to the Ministry of the Environment

Do this **after exact coordinates / municipality are recovered** so the correct office can be selected.

Current routing published by the Ministry of the Environment:

```text
Daisetsuzan National Park Management Office
  other Daisetsuzan areas
  01658-2-2574
  RO-KAMIKAWA@env.go.jp

Higashikawa Ranger Office
  Furano City, Higashikawa Town, Biei Town, Sorachi District
  0166-82-2527
  RO-HIGASHIKAWA@env.go.jp

Kamishihoro Ranger Office
  Kato District, Shintoku Town
  01564-2-3337
  RO-KAMISHIHORO@env.go.jp
```

### Ministry inquiry checklist

Supply one action-specific table rather than a generic statement that the project is ecological research.

| Planned action | Maximum scale | Material retained/removed | Requested determination |
| --- | ---: | --- | --- |
| Phenology / flower census | presurvey + pilot | none | access/research conditions |
| Temporary individual tags | pilot / confirmatory | no biological collection | installation/marking conditions |
| Perfect/male flower removal | registered q manipulation | removed flowers | permit route and quantitative limit |
| Leaf sampling | only if paternity/genotyping retained | leaf tissue | permit route and quantitative limit |
| Moth egg count | all randomized units as needed | none if census only | whether additional authorization applies |
| Moth egg removal | G0 treatment | eggs removed before hatching | exact regulatory treatment at verified zone |
| Fruit/seed assessment | endpoint | clarify whether fruits/seeds are removed from site | permit route if collection is required |

### Draft administrative question

```text
当該地点・地種区分において、上記各行為のうち自然公園法上の許可が必要なものと、許可不要であることを確認できるものを、行為ごとにご教示いただけますでしょうか。必要な場合には、申請様式、必要添付図面、数量の示し方、標準的な申請時期についてもご案内いただけますと幸いです。
```

Do not collapse a verbal answer such as "probably fine" into administrative readiness. Store a written response, permit number, or explicit not-required confirmation in:

```text
empirical/identification_design/PEUCEDANUM_FIELD_ADMIN_READINESS_TEMPLATE_V1.json
```

## Site-recovery record

When the original field team responds, transcribe factual site information into:

```text
empirical/identification_design/PEUCEDANUM_HA_SITE_RECOVERY_TEMPLATE_V1.json
```

Keep the original correspondence separately. Exact sensitive coordinates should not be committed to a public repository if the field team requests restricted handling.

If exact coordinates are sensitive, the public repository should store only:

```text
coordinates_verified = true
municipality
park zone
responsible office
restricted_location_reference = private record ID
```

rather than the coordinates themselves.

## Decision after site recovery

```text
exact HA recovered
+ no conflict with existing long-term study
+ zone / office resolved
          ↓
current project authorizations requested
          ↓
administrative receipt passes
          ↓
HA technical pilot may proceed
```

If HA cannot be shared or manipulated, move to HL / another high-predation Taisetsu population and repeat the same site/permission gate rather than forcing HA.
