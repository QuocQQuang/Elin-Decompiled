# Elin Materials Database

Tài liệu này chứa thông tin chi tiết về tất cả các nguyên liệu (materials) trong game Elin, bao gồm các thuộc tính quan trọng như tier, chance, value, hardness và các đặc tính khác.

## Cấu trúc Dữ liệu Nguyên liệu

Mỗi nguyên liệu trong game Elin được định nghĩa bởi class `SourceMaterial.Row` với các thuộc tính chính:

### Thuộc tính Cơ bản
- **id**: ID số duy nhất của nguyên liệu
- **alias**: Tên bí danh/mã nguyên liệu (được sử dụng trong code)
- **name_JP**: Tên tiếng Nhật
- **name**: Tên tiếng Anh
- **category**: Danh mục nguyên liệu (wood, ore, gem, rock, metal, leather, v.v.)

### Thuộc tính Vật lý
- **hardness**: Độ cứng của nguyên liệu (ảnh hưởng đến damage resistance)
- **weight**: Trọng lượng
- **quality**: Chất lượng cơ bản

### Thuộc tính Kinh tế
- **tier**: Cấp độ nguyên liệu (0-4, càng cao càng hiếm và mạnh)
- **chance**: Xác suất xuất hiện khi random
- **value**: Giá trị kinh tế cơ bản

### Thuộc tính Chiến đấu
- **atk**: Attack modifier
- **dmg**: Damage modifier  
- **dv**: Dodge Value modifier
- **pv**: Protection Value modifier
- **dice**: Dice modifier cho damage

### Thuộc tính Khác
- **tag**: Các tag đặc biệt
- **groups**: Nhóm nguyên liệu (metal, leather, v.v.)
- **elements**: Các element enchantment tự nhiên
- **bits**: Đặc tính đặc biệt (fire-resistant, acid-resistant, v.v.)

## Nguyên liệu Quan trọng được Hardcode

Một số nguyên liệu quan trọng được hardcode trong class `MATERIAL`:

| ID | Alias | Tên | Mô tả |
|----|----|-----|-------|
| 1 | oak | Oak | Gỗ sồi - nguyên liệu gỗ cơ bản |
| 3 | granite | Granite | Đá granite - nguyên liệu đá cơ bản |
| 4 | mud | Mud | Bùn |
| 8 | sand | Sand | Cát |
| 12 | gold | Gold | Vàng - kim loại quý |
| 45 | soil | Soil | Đất |
| 48 | snow | Snow | Tuyết |
| 61 | ice | Ice | Đá |
| 66 | water | Water | Nước |
| 67 | water_fresh | Fresh Water | Nước ngọt |
| 88 | water_sea | Sea Water | Nước biển |

## Hệ thống Tier và Random

### Tier System
Nguyên liệu được chia thành 5 tier (0-4):
- **Tier 0**: Nguyên liệu cơ bản, phổ biến
- **Tier 1**: Nguyên liệu thường, dễ tìm
- **Tier 2**: Nguyên liệu tốt, ít phổ biến hơn
- **Tier 3**: Nguyên liệu hiếm, mạnh
- **Tier 4**: Nguyên liệu siêu hiếm, rất mạnh

### Random Material Selection

Khi game cần chọn nguyên liệu ngẫu nhiên, nó sử dụng các hàm trong `MATERIAL` class:

#### `GetRandomMaterial(lv, group, tryLevelMatTier)`
- **lv**: Level ảnh hưởng đến tier có thể xuất hiện
- **group**: Nhóm nguyên liệu (metal, leather, gem, ore)
- **tryLevelMatTier**: Có match tier với level không

#### Logic Tier Selection:
```
min_tier = (lv >= 60) ? 2 : (lv >= 25) ? 1 : 0
max_tier = Clamp(Random(Random(Random(lv/10 + 2) + 1) + 1), min_tier, 4)
```

Điều này có nghĩa:
- Level < 25: Chỉ có thể lấy tier 0-1
- Level 25-59: Có thể lấy tier 1+
- Level 60+: Có thể lấy tier 2+

#### Weight trong Selection:
Khi chọn nguyên liệu từ tier được quyết định:
```
weight = material.chance * (material.tier == selected_tier ? 5 : 1)
```
Nguyên liệu cùng tier với tier được chọn có xác suất cao gấp 5 lần.

## Danh mục Nguyên liệu

### Categories Chính:
- **wood**: Gỗ các loại
- **ore**: Quặng kim loại
- **gem**: Đá quý
- **rock**: Đá thường
- **bone**: Xương
- **crystal**: Tinh thể
- **soil**: Đất/đá phiến
- **fiber**: Sợi/vải
- **skin**: Da/thuộc da

### Groups:
- **metal**: Kim loại (ore category)
- **leather**: Da thuộc
- **gem**: Đá quý tự nhiên
- **ore**: Quặng chưa chế tạo

## Ảnh hưởng đến Equipment

Khi nguyên liệu được áp dụng lên equipment, nó ảnh hưởng đến stats theo công thức trong `ApplyMaterial()`:

### Damage Calculation:
```
base_damage = source.offense[1] * material.dice / divisor
hit_bonus = source.offense[2] * material.atk / divisor  
damage_bonus = source.offense[3] * material.dmg / divisor
```

### Defense Calculation:
```
dodge_value = source.defense[0] * material.dv / divisor
protection_value = source.defense[1] * material.pv / divisor
```

Với `divisor` phụ thuộc vào rarity:
- Crude: 150
- Normal: 120  
- Superior: 100
- Legendary+: 80

## Shrine Material Selection

Trong hệ thống shrine, nguyên liệu được chọn theo các quy tắc đặc biệt được mô tả trong `docs/shrine_generation_system.md`.

---

**Lưu ý**: Để có danh sách đầy đủ tất cả nguyên liệu với values cụ thể, cần truy cập trực tiếp vào game data files hoặc memory dump, vì thông tin này không được hardcode trong source code mà được load từ external data files.

## Công cụ Trích xuất Dữ liệu

Để trích xuất danh sách đầy đủ các nguyên liệu, có thể sử dụng các method sau trong game:

```csharp
// Truy cập toàn bộ materials
foreach (SourceMaterial.Row material in EClass.sources.materials.rows)
{
    Debug.Log($"ID: {material.id}, Alias: {material.alias}, Name: {material.name}");
    Debug.Log($"Tier: {material.tier}, Chance: {material.chance}, Value: {material.value}");
    Debug.Log($"Category: {material.category}, Hardness: {material.hardness}");
}

// Truy cập materials theo tier
foreach (var tierEntry in SourceMaterial.tierMap)
{
    string groupName = tierEntry.Key;
    SourceMaterial.TierList tierList = tierEntry.Value;
    
    for (int i = 0; i < tierList.tiers.Length; i++)
    {
        foreach (var material in tierList.tiers[i].list)
        {
            Debug.Log($"Group: {groupName}, Tier: {i}, Material: {material.alias}");
        }
    }
}
```

## Các Nguyên liệu Đặc biệt

### Materials với Bits Đặc biệt:
- **fire**: Nguyên liệu chống cháy
- **acid**: Nguyên liệu chống acid

### Materials với Elements:
Một số nguyên liệu có sẵn enchantments tự nhiên được định nghĩa trong field `elements`.

---

*Tài liệu này sẽ được cập nhật khi có thêm thông tin chi tiết về từng nguyên liệu cụ thể từ game data.*
