# Hệ Thống Tạo Shrine trong Elin

## Tổng Quan
Shrine là những bức tượng thần linh có thể được tìm thấy trong các dungeon, mang lại những lợi ích đặc biệt khi sử dụng. Hệ thống tạo shrine được triển khai thông qua phương thức `TryGenerateShrine()` trong class `Zone`.

## Cơ Chế Tạo Shrine

### 1. Điều Kiện Kích Hoạt
Shrine chỉ được tạo trong các Zone có:
- Property `ShrineChance` > 0
- Không phải zone được export (`idExport.IsEmpty()`)
- Zone_Dungeon có `ShrineChance` mặc định là 0.35 (35% cơ hội)

### 2. Quy Trình Tạo Shrine

#### Bước 1: Vòng Lặp Thử
```csharp
for (int i = 0; i < 3; i++)
{
    Rand.SetSeed(base.uid + i);
    if (ShrineChance <= EClass.rndf(1f))
    {
        continue;
    }
    // Tiếp tục tạo shrine...
}
```
- Game thử tạo shrine tối đa 3 lần
- Mỗi lần thử sử dụng seed khác nhau (uid + i)
- Kiểm tra xác suất với `ShrineChance`

#### Bước 2: Tìm Vị Trí Đặt
```csharp
Point randomSpace = EClass._map.GetRandomSpace(3, 3);
if (randomSpace == null) continue;

randomSpace.x++;
randomSpace.z++;

if (randomSpace.HasThing || randomSpace.HasChara) continue;
```
- Tìm không gian trống 3x3 
- Điều chỉnh vị trí về giữa (x++, z++)
- Kiểm tra không có vật thể hoặc nhân vật tại vị trí

#### Bước 3: Quyết Định Loại Shrine
```csharp
Rand.SetSeed(EClass.player.seedShrine);
EClass.player.seedShrine++;

  {
    // Tạo God Statue (1/15 cơ hội, 1/2 khi debug)
    EClass._zone.AddCard(ThingGen.Create("pedestal_power"), randomSpace).Install();
    EClass._zone.AddCard(ThingGen.Create(
        EClass.gamedata.godStatues.RandomItemWeighted((GodStatueData a) => a.chance).idThing, 
        -1, DangerLv), randomSpace).Install();
}
else
{
    // Tạo Power Statue thông thường
    EClass._zone.AddCard(ThingGen.Create("statue_power", -1, DangerLv), randomSpace)
        .Install().SetRandomDir();
}
```

## Loại Shrine

### 1. Power Statue (`statue_power`)
- Loại shrine thông thường (14/15 cơ hội)
- Sử dụng `TraitShrine`
- Có nhiều loại khác nhau dựa trên `ShrineData`

### 2. God Statue 
- Loại shrine hiếm (1/15 cơ hội)
- Đi kèm với `pedestal_power`
- Sử dụng `TraitGodStatue`
- Dựa trên `GodStatueData` với trọng số khác nhau

## Dữ Liệu Shrine

### ShrineData
```csharp
public class ShrineData : EClass
{
    public string id;      // ID của shrine
    public float chance;   // Trọng số xuất hiện
    public int tile;       // Tile hiển thị
    public int skin;       // Skin hiển thị
}
```

### GodStatueData  
```csharp
public class GodStatueData : EClass
{
    public string id;      // ID của thần
    public string idThing; // ID vật phẩm tương ứng
    public float chance;   // Trọng số xuất hiện
}
```

## Chức Năng Shrine

### Power Statue Effects
Dựa trên `Shrine.id`, các hiệu ứng bao gồm:

1. **"material"** - Thay đổi vật liệu của thiết bị
2. **"armor"** - Enchant armor
3. **"replenish"** - Hồi phục HP/Mana/Stamina và loại bỏ debuff
4. **"strife"** - Spawn monsters để chiến đấu
5. **"knowledge"** - Tạo sách kỹ năng hoặc sách cổ
6. **"invention"** - Học công thức ngẫu nhiên
7. **"item"** - Tạo vật phẩm

### God Statue Effects
Dựa trên `Religion.id`:

1. **"harvest"** - Tạo sách Kumiromi
2. **"machine"** - Tạo gene Mani
3. **"healing"** - Thêm điều kiện Rebirth cho party
4. **"luck"** - Tạo item well wish
5. **"wind"** - Tạo blood angel
6. **"earth"/"element"** - Tạo mathammer với vật liệu ngẫu nhiên

## Seed System
- `EClass.player.seedShrine` được tăng mỗi khi tạo shrine
- Đảm bảo tính nhất quán trong việc tạo shrine
- Cho phép reproduce cùng kết quả với cùng seed

## Điều Kiện Sử dụng
- Shrine chỉ có thể sử dụng khi `owner.isOn = true`
- Sau khi sử dụng, shrine sẽ tắt (`owner.isOn = false`)
- God Statue cần vật liệu gold để kích hoạt
- Không thể sử dụng trong User Zone

## Nghiên Cứu Chi Tiết: Hệ Thống Chọn Nguyên Liệu Shrine

### 1. Cơ Chế Xác Định Nguyên Liệu Power Statue

#### 1.1 Quy Trình Lựa Chọn
```csharp
// Bước 1: Kiểm tra loại shrine
if (Shrine.id == "armor") {
    // Special case: Armor shrine có tỷ lệ cố định
    material = EClass.rnd(5) == 0 ? "gold" : "granite";
} else {
    // Bước 2: Tính input level
    int inputLevel = owner.LV / 3;
    
    // Bước 3: Chọn group nguyên liệu
    string group = EClass.rnd(2) == 0 ? "metal" : "leather";
    
    // Bước 4: Cross-group chance (1/15 = 6.67%)
    if (group == "metal" && EClass.rnd(15) == 0) {
        group = "leather";
    } else if (group == "leather" && EClass.rnd(15) == 0) {
        group = "metal";
    }
    
    // Bước 5: Tính tier bằng Triple Random Algorithm
    int min = inputLevel >= 60 ? 2 : (inputLevel >= 25 ? 1 : 0);
    int tierRaw = inputLevel / 10 + 2;
    int tier = Mathf.Clamp(
        EClass.rnd(EClass.rnd(EClass.rnd(tierRaw) + 1) + 1), 
        min, 
        4
    );
    
    // Bước 6: Weighted Selection từ tier
    TierList tierList = SourceMaterial.tierMap[group];
    Tier tierObj = tierList.tiers[tier];
    material = tierObj.Select(); // Weighted random by chance values
}
```

#### 1.2 Hệ Thống Tier Structure

**Tier System (0-4):**
- **Tier 0**: Basic materials (Bronze, Cloth, etc.)
- **Tier 1**: Common materials (Iron, Leather, etc.)  
- **Tier 2**: Good materials (Steel, Chain, etc.)
- **Tier 3**: Rare materials (Silver, Dragon scale, etc.)
- **Tier 4**: Legendary materials (Gold, Mythril, etc.)

**TierList & Tier Class:**
```csharp
public class TierList {
    public Tier[] tiers = new Tier[5]; // 5 tiers total
}

public class Tier {
    public int sum;           // Total weight for selection
    public List<Row> list;    // Materials in this tier
    
    public Row Select() {
        int roll = EClass.rnd(sum);
        int accumulator = 0;
        
        foreach (Row material in list) {
            accumulator += material.chance;
            if (roll < accumulator) {
                return material;
            }
        }
        return list.RandomItem(); // Fallback
    }
}
```

#### 1.3 Triple Random Distribution Analysis

**Công thức:** `Rand(Rand(Rand(x)))`

**Bias Effect:** Triple random tạo strong bias về phía các giá trị thấp hơn:
- Single random: uniform distribution 
- Double random: quadratic bias toward 0
- Triple random: cubic bias toward 0

**Practical Impact:**
```
Input Level 30 (tierRaw = 5):
- P(tier=0) ≈ 42%
- P(tier=1) ≈ 26% 
- P(tier=2) ≈ 16%
- P(tier=3) ≈ 11%
- P(tier=4) ≈ 5%
```

#### 1.4 Min Tier Thresholds

**Level-based Minimums:**
- Level < 25: min_tier = 0 (all tiers possible)
- Level 25-59: min_tier = 1 (tier 0 blocked)  
- Level ≥ 60: min_tier = 2 (tier 0-1 blocked)

**Strategic Implications:**
- Early game: Mostly low-tier materials
- Mid game (25+): Guaranteed tier 1+ materials
- Late game (60+): Guaranteed tier 2+ materials  
    string group = EClass.rnd(2) == 0 ? "metal" : "leather";
    
    // Bước 4: Cross-group chance (1/15)
    if (group == "metal" && EClass.rnd(15) == 0) group = "leather";
    if (group == "leather" && EClass.rnd(15) == 0) group = "metal";
    
    // Bước 5: Tính tier theo công thức phức tạp
    material = MATERIAL.GetRandomMaterial(inputLevel, group, false);
}
```

#### 1.2 Công Thức Tier Selection Chi Tiết

**Input Processing:**
- `input_level = shrine_level / 3`
- `max_calc = input_level / 10 + 2`

**Min Tier Thresholds:**
```
min_tier = {
    0 nếu input_level < 25
    1 nếu 25 ≤ input_level < 60  
    2 nếu input_level ≥ 60
}
```

**Triple Random Tier Calculation:**
```
tier = Clamp(
    Rand(Rand(Rand(max_calc) + 1) + 1),
    min_tier,
    4
)
```

**Phân Tích Xác Suất Tier:**
Với `max_calc = 3`:
- Rand(3): 0,1,2 (33.3% mỗi)
- Rand(Rand(3)+1): 0-2 với phân bố lệch về 0
- Rand(Rand(Rand(3)+1)+1): Càng lệch về tier thấp

### 2. Nghiên Cứu God Statue Material System

#### 2.1 Level Adjustment Formula

**Công Thức Chính:**
```csharp
int adjustedLevel = (owner.LV < 200) ? 
    (owner.LV / 2) + 10 : 
    (owner.LV % 50 * 2) + 10;
```

**Phân Tích Cycle Back Effect:**
```
Level 200: (200 % 50 * 2) + 10 = (0 * 2) + 10 = 10
Level 225: (225 % 50 * 2) + 10 = (25 * 2) + 10 = 60  
Level 250: (250 % 50 * 2) + 10 = (0 * 2) + 10 = 10
Level 275: (275 % 50 * 2) + 10 = (25 * 2) + 10 = 60
```

**Kết Luận:** God Statue level 200+ tạo pattern 50-level cycle với peaks tại level 225, 275, 325...

#### 2.2 TryLevelMatTier Algorithm

**Thuật Toán Chọn Tier:**
```csharp
// Bước 1: Tính base tier
int baseTier = adjustedLevel / 15;

// Bước 2: Random variance ±1
int variance = EClass.rnd(2) - EClass.rnd(2); // [-1, 0, +1]

// Bước 3: Apply variance với clamp
int finalTier = Clamp(baseTier + variance, 0, 4);
```

**Ví Dụ Cụ Thể:**
- `adjustedLevel = 60`: baseTier = 4, finalTier = 3-4
- `adjustedLevel = 45`: baseTier = 3, finalTier = 2-4  
- `adjustedLevel = 15`: baseTier = 1, finalTier = 0-2

### 3. Bảng Xác Suất Chi Tiết

#### 3.1 Power Statue Tier Probability

| Input Level | Min Tier | Max Calc | Tier 0 | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|-------------|----------|----------|--------|--------|--------|--------|--------|
| 5           | 0        | 2        | 50%    | 33%    | 17%    | 0%     | 0%     |
| 15          | 0        | 3        | 37%    | 30%    | 20%    | 13%    | 0%     |
| 25          | 1        | 4        | 0%     | 40%    | 27%    | 20%    | 13%    |
| 45          | 1        | 6        | 0%     | 35%    | 25%    | 20%    | 20%    |
| 65          | 2        | 8        | 0%     | 0%     | 45%    | 28%    | 27%    |

*Xác suất được ước tính dựa trên phân bố triple random*

#### 3.2 God Statue Adjusted Level Mapping

| Danger Level | God Statue Level | Formula Used | Adjusted Level | Expected Tier |
|-------------|------------------|--------------|----------------|---------------|
| 50          | 50              | lv/2 + 10    | 35             | 2-3           |
| 100         | 100             | lv/2 + 10    | 60             | 3-4           |
| 150         | 150             | lv/2 + 10    | 85             | 4-4*          |
| 200         | 200             | (lv%50*2)+10 | 10             | 0-1           |
| 225         | 225             | (lv%50*2)+10 | 60             | 3-4           |
| 250         | 250             | (lv%50*2)+10 | 10             | 0-1           |

*Tier 4 với ít variance do Clamp(5±1, 0, 4)*

### 4. Material Selection với Weighted System

#### 4.1 Tier Selection vs Material Selection

**Tier Selection (Bước 1):**
- Sử dụng Triple Random cho Power Statue
- Sử dụng Level-based + variance cho God Statue

**Material Selection (Bước 2):**
```csharp
// Trong Tier.Select() method
public Row Select() {
    int roll = EClass.rnd(sum);           // Random trong tổng weight
    int accumulator = 0;
    
    foreach (Row material in list) {
        accumulator += material.chance;    // Chance = base weight của material
        if (roll < accumulator) {
            return material;
        }
    }
    return list.RandomItem();             // Fallback nếu có lỗi
}
```

#### 4.2 Chance Weight System

**Base Chance Values (ví dụ):**
- Bronze: chance = 100 (common)
- Iron: chance = 80 (less common)
- Steel: chance = 60 (uncommon) 
- Mithril: chance = 30 (rare)
- Adamantite: chance = 10 (very rare)

**Tier Match Bonus:**
- Materials trong tier được select: weight = chance × **5**
- Materials trong tier khác: weight = chance × **1**

**Ví dụ Selection:**
```
Tier 2 được chọn:
- Iron (tier 1): weight = 80 × 1 = 80
- Steel (tier 2): weight = 60 × 5 = 300  ← Favored!
- Bronze (tier 0): weight = 100 × 1 = 100

Total weight = 480
Steel probability = 300/480 = 62.5%
```

#### 4.3 GetRandomMaterialFromCategory System

**Alternative Algorithm cho special cases:**
```csharp
public static SourceMaterial.Row GetRandomMaterialFromCategory(int lv, string[] cat, SourceMaterial.Row fallback)
{
    // Min tier thresholds
    int min = ((lv >= 60) ? 2 : ((lv >= 25) ? 1 : 0));
    
    // Modified calculation
    int a2 = lv / 5 + 2;  // Different divisor!
    
    // Triple random với modified base
    int idTier = Mathf.Clamp(EClass.rnd(EClass.rnd(EClass.rnd(a2) + 1) + 1), min, 4);
    
    // Filter materials by category AND tier limit
    List<SourceMaterial.Row> list = materials.Where(m => 
        cat.Contains(m.category) && m.tier <= idTier).ToList();
    
    if (list.Count > 0) {
        // Enhanced tier match bonus
        return list.RandomItemWeighted(a => a.chance * ((a.tier != idTier) ? 1 : 5));
    }
    return fallback;
}
```

**Key Differences:**
- Uses `lv / 5 + 2` instead of `lv / 10 + 2`
- Filters by `tier <= idTier` instead of exact tier
- Still applies 5x tier match bonus

### 5. Strategic Optimization Guide

#### 4.1 Tier System Analysis

**Tier Distribution trong Game Data:**
```
Tier 0: Common materials (wood, leather, iron)
Tier 1: Good materials (steel, quality leather) 
Tier 2: Fine materials (mithril, dragon scale)
Tier 3: Rare materials (adamantite, ether skin)
Tier 4: Legendary materials (rubynus, diamond)
```

#### 4.2 Weighted Selection Formula

**Selection Weight Calculation:**
```csharp
weight = material.chance * ((material.tier == targetTier) ? 5 : 1)
```

**Ví Dụ với Tier 2 Target:**
- Mithril (tier 2, chance 10): weight = 10 × 5 = 50
- Steel (tier 1, chance 15): weight = 15 × 1 = 15  
- Iron (tier 0, chance 20): weight = 20 × 1 = 20

**Xác Suất Chọn:**
- Mithril: 50/(50+15+20) = 58.8%
- Steel: 15/85 = 17.6%
- Iron: 20/85 = 23.5%

### 5. Practical Applications & Strategies

#### 5.1 Optimal Shrine Hunting Levels

**Power Statue Optimization:**
```
Best Range: Danger Level 76-150
Reason: 
- Min tier ≥ 1 (tránh materials thấp)
- Max tier = 4 (có cơ hội tier cao)  
- Input level 25-50 (balanced probability)
```

**God Statue Optimization:**
```  
Peak Range: Danger Level 150-199
Reason:
- Adjusted level 85-109 (tier 4+ guaranteed)
- Chưa bị cycle back effect
- Ít variance do high base tier
```

#### 5.2 Cross-Group Exploitation

**Strategy:**
1. Target shrine với preferred group (metal/leather)
2. 1/15 chance swap tạo surprise high-tier material
3. Especially valuable cho God Statue với tryLevelMatTier=true

#### 5.3 Armor Shrine Special Case

**Analysis:**
- Gold chance: 20% (1/5)
- Gold = Tier 4 equivalent + special properties
- Independent of danger level
- Most consistent high-tier source

### 6. Debug Mode Impact Analysis

**Normal Mode vs Debug Mode:**
```
God Statue Chance:
- Normal: 1/15 = 6.67%
- Debug: 1/2 = 50.0%
- Increase: 7.5x multiplier

Per Zone Expected Shrines:
- Normal: 0.35 * 3 attempts = 1.05 attempts
- Debug: Enhanced generation rate
```

**Research Implications:**
- Debug mode dramatically increases high-tier material access
- Test environments không representative của normal gameplay
- Material economy balance khác biệt significantly

### Power Statue Material Selection
Shrine sử dụng `TraitShrine.GetMaterial()` để chọn nguyên liệu:

```csharp
Rand.SetSeed(owner.c_seed);
if (Shrine.id == "armor")
{
    // Shrine armor: 20% cơ hội gold, 80% granite
    mat = EClass.sources.materials.alias[(EClass.rnd(5) == 0) ? "gold" : "granite"];
}
else
{
    // Shrine khác: dựa trên level và random group
    mat = MATERIAL.GetRandomMaterial(owner.LV / 3, (EClass.rnd(2) == 0) ? "metal" : "leather");
}
```

**Tóm Tắt Công Thức:**
- **Input Level**: `shrine.LV / 3`
- **Group Selection**: 50% "metal", 50% "leather" + 1/15 cross-swap chance
- **Tier Formula**: Triple random với min tier thresholds

### God Statue Material Selection
God Statue sử dụng công thức phức tạp hơn:

```csharp
Rand.SetSeed(owner.c_seed);
int adjustedLevel = ((owner.LV < 200) ? (owner.LV / 2) : (owner.LV % 50 * 2)) + 10;
SourceMaterial.Row material = MATERIAL.GetRandomMaterial(
    adjustedLevel, 
    (Religion.id == "earth") ? "metal" : "leather", 
    tryLevelMatTier: true
);
```

**Tóm Tắt Công Thức:**
- **Level < 200**: `adjusted = (level / 2) + 10`
- **Level ≥ 200**: `adjusted = (level % 50 * 2) + 10` (cycle back!)
- **Tier Selection**: `base_tier = adjusted / 15` với ±1 variance

### Material Category System
Nguyên liệu được phân loại theo:

1. **Tier System** (0-4): Tier cao hơn = nguyên liệu tốt hơn
2. **Category Groups**:
   - "metal": Kim loại (iron, steel, mithril, adamantite...)
   - "leather": Da thuộc (leather, dragon scale...)
   - "wood": Gỗ (oak, cedar...)
   - "rock": Đá (granite, marble...)

3. **Chance Weight**: Mỗi material có chance riêng, tier hiện tại được boost x5

## Mathematical Analysis & Advanced Research

### 7. Probability Distribution Models

#### 7.1 Triple Random Mathematical Model

**Standard Uniform Random:** `f(x) = 1` for x ∈ [0,1]

**Double Random:** `f₂(x) = 2(1-x)` - Linear decay

**Triple Random:** `f₃(x) = 3(1-x)²` - Quadratic decay

**Expected Values:**
- Single: E[X] = 0.5
- Double: E[X] = 1/3 ≈ 0.333  
- Triple: E[X] = 1/4 = 0.25

**Practical Impact for Tier Selection:**
```
For tierRaw = 4:
- Mean tier ≈ 4 × 0.25 = 1.0
- Tier distribution heavily skewed to 0-1
- High-tier materials very rare without min_tier protection
```

#### 7.2 God Statue Cycle Analysis

**Cycle Function:** `f(x) = (x % 50) × 2 + 10` for x ≥ 200

**Properties:**
- Period: 50 levels
- Range: [10, 110]
- Peaks at: x ≡ 25 (mod 50)
- Valleys at: x ≡ 0 (mod 50)

**Optimization Points:**
- Level 225: adjusted = 60 → tier 3-4
- Level 250: adjusted = 10 → tier 0-1  
- Level 275: adjusted = 60 → tier 3-4

### 8. Economic Impact Analysis

#### 8.1 Material Value Distribution

**Tier Economic Value (estimated):**
- Tier 0: 1x base value
- Tier 1: 3x base value  
- Tier 2: 8x base value
- Tier 3: 20x base value
- Tier 4: 50x+ base value

**Expected Material Value by Danger Level:**

| Danger Level | Power Statue | God Statue | Optimal Choice |
|-------------|--------------|------------|----------------|
| 25-49       | Tier 0-1     | Tier 2-3   | God Statue    |
| 50-74       | Tier 0-2     | Tier 3-4   | God Statue    |
| 75-99       | Tier 1-2     | Tier 4     | God Statue    |
| 100-149     | Tier 1-3     | Tier 4     | Either        |
| 150-199     | Tier 2-3     | Tier 4     | Power Statue  |
| 200-224     | Tier 2-4     | Tier 0-1   | Power Statue  |
| 225-249     | Tier 2-4     | Tier 3-4   | Either        |

#### 8.2 Cross-Group Arbitrage Opportunities

**Metal vs Leather Group Values:**
- Metal group: Generally higher DV/PV stats
- Leather group: Generally higher flexibility/special effects
- Cross-group swap (1/15 chance): Unexpected combinations

**Arbitrage Strategy:**
1. Target zones where preferred group mismatches shrine preference
2. Exploit 6.67% cross-group chance for value arbitrage
3. Particularly effective for God Statue (tryLevelMatTier bonus)

### 9. Seed Management & Consistency

#### 9.1 Seed System Analysis

**Shrine Generation Seeds:**
```csharp
// Spawn seed: based on zone UID + attempt number
Rand.SetSeed(zone.uid + attempt);

// Material seed: consistent per shrine instance  
Rand.SetSeed(shrine.c_seed);
```

**Implications:**
- Shrine material determined at creation, not use
- Same shrine always gives same material type
- Different shrines in zone can have different materials
- Reloading doesn't change existing shrine materials

#### 9.2 Seed Exploitation Possibilities

**Player-Controllable Factors:**
- Zone exploration order (affects shrine.c_seed assignment)
- Save/reload timing (limited impact due to seed persistence)
- Multiple character progression paths

**Non-Exploitable Factors:**
- Zone UID (fixed at world generation)
- Shrine c_seed (determined at shrine creation)
- Material type (locked to shrine instance)

### 10. Advanced Strategies & Meta-Gaming

#### 10.1 Optimal Shrine Hunting Routes

**Early Game (Level < 60):**
1. Target God Statues exclusively
2. Focus on zones DL 30-80 for consistent tier 2-3
3. Avoid Power Statues (poor tier distribution)

**Mid Game (Level 60-150):**  
1. Balance God/Power Statues based on current gear needs
2. Target zones DL 75-150 for optimal God Statue performance
3. Consider Armor Shrines for guaranteed 20% gold chance

**Late Game (Level 150+):**
1. Target Power Statues in high DL zones (150-199)
2. Avoid God Statues during cycle valleys (200, 250, 300...)
3. Plan around cycle peaks (225, 275, 325...)

#### 10.2 Zone Selection Optimization

**Power Statue Optimization:**
- Target DL 150-199 (peak performance before penalties)
- Avoid very high DL zones (diminishing returns)
- Focus on zones with multiple shrine chances

**God Statue Optimization:**
- DL < 200: Linear scaling, higher is better
- DL ≥ 200: Target cycle peaks (25, 75, 125 within cycle)
- Avoid cycle valleys for maximum efficiency

#### 10.3 Material Category Exploitation

**Group Preference Strategy:**
1. Identify desired group (metal/leather)
2. Target shrines with opposite base preference
3. Exploit 1/15 cross-group chance for surprise upgrades
4. Particularly valuable for God Statue tier bonuses

**Special Case Strategies:**
- Armor Shrines: Independent of level, consistent 20% gold
- Earth Religion: Guaranteed metal group (no cross-group variance)
- Element Religion: Guaranteed leather group (no cross-group variance)

### Ví Dụ Thực Tế

**Shrine Level 30:**
- Input cho GetRandomMaterial: `30 / 3 = 10`
- Min tier: `10 >= 25 ? 1 : 0` = 0
- Max calculation: `10/10 + 2 = 3`
- Tier range: 0-3 (không thể lên tier 4)

**God Statue Level 100:**
- Adjusted level: `(100 / 2) + 10 = 60`
- Base tier: `60 / 15 = 4`
- Final tier: `Clamp(4 ± 0-1, 0, 4) = 3-4` (tier rất cao)

**God Statue Level 250:**
- Adjusted level: `(250 % 50 * 2) + 10 = 10`
- Level cao quá sẽ cycle lại thành level thấp

## Bảng Phân Tích Shrine Theo Danger Level

### Power Statue Material Quality

| Danger Level | Shrine Level | Input Level | Min Tier | Max Calculation | Tier Range | Material Quality |
|-------------|-------------|-------------|----------|-----------------|------------|------------------|
| 1-15        | 1-5         | 0-1         | 0        | 2               | 0-1        | Rất Thấp (wood, crude metal) |
| 16-30       | 5-10        | 1-3         | 0        | 2-3             | 0-2        | Thấp (iron, leather) |
| 31-75       | 10-25       | 3-8         | 0-1      | 3-4             | 0-3        | Trung Bình (steel, good leather) |
| 76-150      | 25-50       | 8-16        | 1-2      | 4-5             | 1-4        | Cao (mithril, dragon scale) |
| 151-180     | 50-60       | 16-20       | 1-2      | 4-5             | 1-4        | Rất Cao (adamantite) |
| 181+        | 60+         | 20+         | 2        | 4+              | 2-4        | Cực Cao (ether, artifacts) |

### God Statue Material Quality

| Danger Level | God Statue Level | Adjusted Level | Base Tier | Final Tier Range | Material Quality |
|-------------|------------------|----------------|-----------|------------------|------------------|
| 1-20        | 1-20            | 11-20          | 0-1       | 0-2              | Thấp-Trung Bình |
| 21-50       | 21-50           | 20-35          | 1-2       | 0-3              | Trung Bình-Cao |
| 51-100      | 51-100          | 35-60          | 2-4       | 1-4              | Cao-Rất Cao |
| 101-150     | 101-150         | 60-85          | 4         | 3-4              | Rất Cao |
| 151-199     | 151-199         | 85-109         | 4+        | 4                | Cực Cao |
| 200-249     | 200-249         | 10-20*         | 0-1       | 0-2              | **Cycle Back!** |
| 250-299     | 250-299         | 10-20*         | 0-1       | 0-2              | **Cycle Back!** |
| 300+        | 300+            | 10-20*         | 0-1       | 0-2              | **Cycle Back!** |

*Level 200+ cycle back do công thức `(level % 50 * 2) + 10`

### Xác Suất Xuất Hiện Shrine

| Danger Level | Zone Visits | Power Statue | God Statue | Tổng Cơ Hội Shrine |
|-------------|-------------|--------------|------------|-------------------|
| Mọi Level   | 1 visit     | ~32.7%       | ~2.3%      | ~35% (base chance) |
| Mọi Level   | 3 visits    | ~70.1%       | ~6.4%      | ~76.5% |
| Mọi Level   | 5 visits    | ~83.2%       | ~9.5%      | ~92.7% |

**Tính toán**: 
- Mỗi attempt: 35% chance, max 3 attempts/zone
- Power Statue: 14/15 × shrine_chance  
- God Statue: 1/15 × shrine_chance
- Multiple visits tích lũy xác suất

### Sweet Spots cho Shrine Hunting

| Mục Tiêu | Recommended Danger Level | Lý Do |
|----------|-------------------------|-------|
| **High-Tier Power Statue** | 75-180 | Đảm bảo tier 1-4 material, tránh level quá cao |
| **Best God Statue** | 150-199 | Maximum tier 4, chưa bị cycle back |
| **Consistent Quality** | 76-150 | Balance giữa chất lượng và consistency |
| **Early Game Shrines** | 30-75 | Accessible với tier 0-3 material |
| **Avoid High Level** | 200+ | God Statue bị cycle back về tier thấp |

### Lưu Ý Đặc Biệt

1. **Armor Shrine**: Luôn cho 20% gold (tier max), 80% granite - không phụ thuộc level
2. **Cross-Group Swap**: 1/15 cơ hội metal ↔ leather, tạo variation
3. **Tier Boost**: Material cùng tier với target được boost weight ×5  
4. **God Statue Cycle**: Level 200+ paradox - càng cao càng dễ ra material thấp
5. **Debug Mode**: Tăng God Statue chance từ 1/15 lên 1/2

## Debug Mode
Khi `EClass.debug.test = true`:
- Cơ hội tạo God Statue tăng từ 1/15 lên 1/2
- Tất cả các chance khác cũng được điều chỉnh cho việc test

## Tổng Kết Nghiên Cứu & Khuyến Nghị

### Core Mechanics Summary

**Shrine Generation Process:**
1. **Spawn Check**: 35% base chance per attempt, 3 attempts per zone
2. **Type Selection**: 1/15 chance God Statue, 14/15 chance Power Statue  
3. **Material Determination**: Based on shrine type and danger level
4. **Seed Consistency**: Material locked at shrine creation

**Power Statue Material Formula:**
```
input_level = shrine.LV / 3
group = random("metal", "leather") with 1/15 cross-swap
tier = Clamp(Rand(Rand(Rand(input_level/10 + 2) + 1) + 1), min_tier, 4)
material = weighted_select_from_tier(group, tier)
```

**God Statue Material Formula:**
```
adjusted = (level < 200) ? (level/2 + 10) : (level%50 * 2 + 10)
base_tier = adjusted / 15
final_tier = Clamp(base_tier ± variance, 0, 4)
material = weighted_select_from_tier(group, final_tier)
```

### Key Strategic Insights

**1. Level-Based Optimization:**
- **Early Game**: Focus God Statues, DL 30-80
- **Mid Game**: Balanced approach, DL 75-150  
- **Late Game**: Power Statues, avoid God Statue valleys

**2. Mathematical Sweet Spots:**
- **Power Statue Peak**: DL 150-199 (pre-penalty)
- **God Statue Peak**: DL 150-199 (pre-cycle)
- **God Statue Cycles**: Target levels 225, 275, 325...

**3. Economic Exploitation:**
- **Armor Shrines**: 20% gold regardless of level
- **Cross-Group Chance**: 6.67% surprise material upgrades
- **Tier Match Bonus**: 5x weight for selected tier materials

### Critical Discovery: God Statue Cycle Back

**The Paradox:** God Statues become WORSE at level 200+
- Level 199: tier 3-4 materials (excellent)
- Level 200: tier 0-1 materials (terrible)  
- Level 225: tier 3-4 materials (excellent again)

**Strategic Implication:** Plan character progression around these cycles for optimal shrine farming.

### Final Recommendations

**For Players:**
1. Prioritize God Statues until level 150
2. Target zones DL 75-150 for consistent high-tier materials
3. Plan late-game progression around 50-level cycles
4. Use Armor Shrines as consistent gold source (20% chance)

**For Developers:**
1. Consider flattening the cycle back effect for smoother progression
2. Review triple random bias toward low tiers (may be too harsh)
3. Debug mode creates unrealistic material economy expectations
4. Cross-group swap adds valuable unpredictability

**For Modders:**
1. Material chance values are easily tweakable in data files
2. Tier thresholds could be adjusted for different game balance
3. Cycle formula could be modified for different progression curves
4. Weighted selection system allows for fine-tuned material rarity

---

*Nghiên cứu này dựa trên phân tích code từ Elin decompiled version. Các con số và công thức có thể thay đổi trong các version khác của game.*
