# Changelog Cursor - Elin Decompiled

## Version 1.5.0 - Material Database Documentation (2025-01-19)

### Added
- **Comprehensive Material Database**: `docs/material_database.md`
  - Detailed documentation of Elin's material system và SourceMaterial.Row structure
  - Complete breakdown of material properties: tier, chance, value, hardness, combat stats
  - Material categories analysis: wood, ore, gem, rock, bone, crystal, soil, fiber, skin
  - Group classification system: metal, leather, gem, ore với cross-group mechanics
  - Hardcoded materials reference table (oak, granite, gold, water variants)

### Material System Analysis
- **Tier System Deep Dive**: 5-tier classification (0-4) với rarity implications
- **Random Selection Algorithms**: GetRandomMaterial() và GetRandomMaterialFromCategory()
- **Equipment Impact Formulas**: Damage và defense calculation với material modifiers
- **Weight Selection Logic**: chance × (tier_match ? 5 : 1) weighting system
- **Level-Based Tier Constraints**: Min tier progression with level thresholds

### Technical Infrastructure
- **SourceMaterial.Row Properties**: Complete field documentation
- **TierList và Tier Classes**: Internal organization structure
- **Material Application**: ApplyMaterial() impact on equipment stats
- **Element System Integration**: Natural enchantments trong materials
- **Special Bits System**: Fire-resistant, acid-resistant properties

### Reference Information  
- **Material IDs**: Key materials với their numeric IDs
- **Category Classifications**: Complete category breakdown với usage patterns
- **Extraction Tools**: Code examples for material data mining
- **Shrine Integration**: Cross-reference với shrine material selection system

### Economic Analysis
- **Value System**: Material value calculations và economic implications  
- **Tier-Value Correlation**: Higher tier = exponentially higher value
- **Category Value Differences**: Metal vs leather vs gem economic positioning
- **Crafting Impact**: Material choice effects on final product value

## Version 1.4.0 - Advanced Mathematical Analysis & Strategic Meta-Gaming (2025-01-19)

### Added
- **Mathematical Analysis Section**: Comprehensive mathematical modeling của shrine system
  - Triple random probability distribution models với expected values
  - God Statue cycle function analysis: `f(x) = (x % 50) × 2 + 10`
  - Economic impact analysis với material value distribution
  - Seed management system documentation với exploitation analysis

### Advanced Research
- **Weighted Selection Deep Dive**: Complete analysis của material selection algorithm
  - Tier selection vs material selection separation
  - Chance weight system với 5x tier match bonus
  - GetRandomMaterialFromCategory alternative algorithm
  - Base chance values và weight calculation examples

### Strategic Meta-Gaming
- **Optimal Shrine Hunting Routes**: Level-based strategy recommendations
  - Early game (< 60): God Statue focus, DL 30-80
  - Mid game (60-150): Balanced approach, DL 75-150
  - Late game (150+): Power Statue preference, avoid cycle valleys
- **Zone Selection Optimization**: Mathematical approach to shrine farming
- **Cross-Group Arbitrage**: Economic exploitation của 1/15 cross-group chance

### Economic Analysis
- **Material Value Distribution**: Tier-based economic value estimates
- **Expected Material Value by Danger Level**: Comprehensive comparison table
- **Cross-Group Arbitrage Opportunities**: Metal vs Leather value analysis

### Technical Insights
- **Probability Distribution Models**: Mathematical formulas cho tier distribution
- **Seed System Analysis**: Shrine generation vs material seeds
- **Seed Exploitation Possibilities**: Player-controllable vs non-exploitable factors

### Advanced Strategies
- **Material Category Exploitation**: Group preference strategy
- **Special Case Strategies**: Armor Shrines, Earth/Element Religion analysis
- **Cycle Awareness**: God Statue level planning cho optimal material quality

## Version 1.3.0 - Deep Material Selection Research & Formulas (2025-01-19)

### Added
- **Nghiên Cứu Chi Tiết Hệ Thống Chọn Nguyên Liệu**: Phân tích sâu về material selection
  - Quy trình lựa chọn nguyên liệu từng bước với code examples
  - Triple random tier calculation analysis với xác suất chi tiết
  - God Statue cycle back effect research với pattern mapping
  - TryLevelMatTier algorithm breakdown
  - Weighted selection formula với ví dụ tính toán cụ thể

### Research Findings
- **Power Statue Tier Probability Table**: Xác suất từng tier theo input level
- **God Statue Cycle Pattern**: 50-level cycle với peaks tại 225, 275, 325...
- **Material Weight Formula**: `weight = chance × (tier_match ? 5 : 1)`
- **Cross-Group Exploitation**: 1/15 chance tạo surprise high-tier materials
- **Armor Shrine Analysis**: 20% gold independent của danger level

### Mathematical Models
- **Triple Random Distribution**: Phân tích `Rand(Rand(Rand(x)))` bias toward lower values
- **Variance Effect**: ±1 random trong God Statue tier selection
- **Min Tier Thresholds**: Level 25→tier≥1, Level 60→tier≥2
- **Cycle Back Formula**: `(level % 50 * 2) + 10` tạo sawtooth pattern

### Practical Applications
- **Optimal Hunting Strategies**: DL 76-150 cho Power, DL 150-199 cho God Statue
- **Debug Mode Impact**: 7.5x God Statue multiplier analysis
- **Material Economy**: Balance implications cho normal vs debug gameplay

### Technical Deep Dive
- **Seed Management**: c_seed usage cho material consistency
- **Tier System**: 5-tier classification với examples
- **Group Selection**: Metal/leather distribution với cross-swap mechanics

## Version 1.2.0 - Comprehensive Shrine-Danger Level Analysis Tables (2025-01-19)

### Added
- **Bảng phân tích Shrine theo Danger Level**: Mapping chi tiết giữa danger level và chất lượng shrine
  - Power Statue material quality table (6 tier ranges từ danger 1-181+)
  - God Statue material quality table với cycle back analysis  
  - Shrine appearance probability table theo số lần visit zone
  - Sweet spots recommendation cho shrine hunting strategy

### Major Analysis
- **Power Statue Sweet Spot**: Danger Level 75-180 cho tier 1-4 materials
- **God Statue Peak**: Danger Level 150-199 trước khi cycle back
- **Cycle Back Paradox**: Danger Level 200+ làm God Statue material trở về tier thấp
- **Probability Mapping**: 35% base chance → 76.5% sau 3 visits → 92.7% sau 5 visits

### Strategic Insights
- **Early Game**: DL 30-75 accessible với tier 0-3
- **End Game**: DL 76-150 balance optimal 
- **Avoid Zone**: DL 200+ paradox effect
- **Special Cases**: Armor shrine không phụ thuộc level (20% gold)

### Practical Applications
- Shrine hunting route optimization
- Material quality prediction
- Risk/reward analysis cho dungeon exploration
- Debug mode impact quantification (1/15 → 1/2 God Statue)

## Version 1.1.0 - Enhanced Shrine Material System Documentation (2025-01-19)

### Added
- **Hệ thống chọn nguyên liệu cho Shrine**: Chi tiết hoàn chỉnh về cách game chọn nguyên liệu
  - Power Statue material selection với công thức toán học cụ thể
  - God Statue material selection với level adjustment formula
  - Tier calculation system với ví dụ thực tế
  - Material category và chance weight system

### Enhanced
- **Công thức toán học trực quan**:
  - Tier calculation: `Clamp(Rand(Rand(Rand(level/10 + 2) + 1) + 1), min_tier, 4)`
  - God Statue level adjustment: `level < 200 ? (level/2) + 10 : (level%50 * 2) + 10`
  - Min tier thresholds: level ≥60 → tier≥2, level ≥25 → tier≥1
  - Cross-group chance: 1/15 (metal ↔ leather swap)

### Technical Analysis
- Analyzed `MATERIAL.cs` GetRandomMaterial() methods
- Studied `TraitShrine.GetMaterial()` implementation  
- Investigated God Statue material formula in `TraitGodStatue.cs`
- Documented tier system và weighted selection

### Examples Added
- Shrine Level 30 → input 10 → tier range 0-3
- God Statue Level 100 → adjusted 60 → tier 3-4  
- God Statue Level 250 → cycles back to low level due to modulo

## Version 1.0.0 - Shrine Generation System Documentation (2025-01-19)

### Added
- **Tài liệu hệ thống tạo Shrine**: `docs/shrine_generation_system.md`
  - Phân tích chi tiết cơ chế tạo shrine trong Zone_Dungeon
  - Giải thích quy trình 3 bước: kiểm tra điều kiện, tìm vị trí, quyết định loại shrine
  - Mô tả 2 loại shrine: Power Statue (14/15 cơ hội) và God Statue (1/15 cơ hội)
  - Chi tiết về ShrineData và GodStatueData structure
  - Liệt kê tất cả effects của shrine theo loại
  - Giải thích seed system và debug mode
  - Điều kiện sử dụng shrine

### Technical Details
- Phân tích code từ `Zone.cs` method `TryGenerateShrine()`
- Nghiên cứu `TraitShrine.cs` và `TraitGodStatue.cs`  
- Tìm hiểu `ShrineData.cs` và `GodStatueData.cs`
- Khám phá cơ chế spawn và effect system

### Implementation Notes
- Shrine generation sử dụng weighted random selection
- Mỗi zone có thể tạo tối đa 3 shrine attempts
- Debug mode tăng đáng kể cơ hội tạo God Statue (từ 1/15 lên 1/2)
- System sử dụng player seed để đảm bảo consistency
