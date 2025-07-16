import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from typing import Dict, List, Tuple
import random

class MaterialTierAnalyzer:
    """Phân tích phân phối tier của material theo danger level"""
    
    def __init__(self):
        self.max_tier = 4
        self.samples = 10000000
        
    def simulate_old_formula(self, lv: int) -> int:
        """Mô phỏng công thức cũ: EClass.rnd(EClass.rnd(EClass.rnd(lv / 10 + 2) + 1) + 1)"""
        # Áp dụng cho owner.LV / 3
        effective_lv = lv // 3
        
        # Công thức cũ
        base = effective_lv // 10 + 2
        rand1 = random.randint(0, max(0, base - 1))
        rand2 = random.randint(0, max(0, rand1))
        rand3 = random.randint(0, max(0, rand2))
        
        # Áp dụng minimum tier
        min_tier = self.get_minimum_tier(effective_lv)
        max_tier_available = min(self.max_tier, 5)  # Giả sử có 6 tier (0-5)
        
        return max(min_tier, min(rand3, max_tier_available))
    
    def simulate_new_formula_exponential(self, lv: int, tier_bias: float = 0.3) -> int:
        """Mô phỏng công thức mới: exponential distribution"""
        effective_lv = lv // 3
        
        # Normalize level to 0-1 range
        normalized_level = min(effective_lv / 100.0, 1.0)
        
        # Base tier calculation using exponential curve
        base_tier = (normalized_level ** 2) * self.max_tier
        
        # Add randomness with weighted distribution
        random_factor = (random.random() - 0.5) * 2  # -1 to 1
        tier_variation = random_factor * (1 - tier_bias) * 2
        
        # Final tier calculation
        final_tier = base_tier + tier_variation
        
        # Apply minimum tier
        min_tier = self.get_minimum_tier(effective_lv)
        
        return max(min_tier, min(round(final_tier), self.max_tier))
    
    def simulate_new_formula_logarithmic(self, lv: int) -> int:
        """Mô phỏng công thức mới: logarithmic distribution"""
        effective_lv = lv // 3
        
        if effective_lv <= 0:
            return 0
            
        # Logarithmic scaling
        log_base = 1.5
        scaled_level = np.log(effective_lv + 1) / np.log(log_base)
        normalized_tier = scaled_level / (np.log(101) / np.log(log_base))
        
        # Add controlled randomness
        random_bonus = (random.randint(0, 2) - 1) * 0.3  # -0.3 to 0.6
        final_tier = (normalized_tier + random_bonus) * self.max_tier
        
        min_tier = self.get_minimum_tier(effective_lv)
        return max(min_tier, min(round(final_tier), self.max_tier))
    
    def get_minimum_tier(self, level: int) -> int:
        """Xác định tier tối thiểu dựa trên level"""
        if level >= 80:
            return 3
        elif level >= 60:
            return 2
        elif level >= 25:
            return 1
        return 0
    
    def analyze_tier_distribution(self, danger_levels: List[int], method: str = "old") -> Dict[int, Dict[int, float]]:
        """Phân tích phân phối tier cho các danger level"""
        results = {}
        
        for danger_lv in danger_levels:
            tier_counts = {i: 0 for i in range(self.max_tier + 1)}
            
            for _ in range(self.samples):
                if method == "old":
                    tier = self.simulate_old_formula(danger_lv)
                elif method == "exponential":
                    tier = self.simulate_new_formula_exponential(danger_lv)
                elif method == "logarithmic":
                    tier = self.simulate_new_formula_logarithmic(danger_lv)
                
                if tier <= self.max_tier:
                    tier_counts[tier] += 1
            
            # Convert to percentages
            results[danger_lv] = {
                tier: (count / self.samples) * 100 
                for tier, count in tier_counts.items()
            }
        
        return results
    
    def create_visualization(self, danger_levels: List[int]):
        """Tạo biểu đồ trực quan so sánh các phương pháp"""
        
        # Analyze all methods
        old_results = self.analyze_tier_distribution(danger_levels, "old")
        exp_results = self.analyze_tier_distribution(danger_levels, "exponential")
        log_results = self.analyze_tier_distribution(danger_levels, "logarithmic")
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Material Tier Distribution Analysis\n(Formula: owner.LV / 3)', fontsize=16, fontweight='bold')
        
        # Method 1: Old Formula
        self._plot_heatmap(old_results, danger_levels, axes[0,0], "Old Formula (Triple Random)")
        
        # Method 2: New Exponential
        self._plot_heatmap(exp_results, danger_levels, axes[0,1], "New Exponential Formula")
        
        # Method 3: New Logarithmic
        self._plot_heatmap(log_results, danger_levels, axes[1,0], "New Logarithmic Formula")
        
        # Method 4: Comparison Line Chart
        self._plot_comparison(old_results, exp_results, log_results, danger_levels, axes[1,1])
        
        plt.tight_layout()
        plt.savefig('tier_distribution_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Create detailed statistics table
        self._create_statistics_table(old_results, exp_results, log_results, danger_levels)
    
    def _plot_heatmap(self, results: Dict[int, Dict[int, float]], danger_levels: List[int], ax, title: str):
        """Vẽ heatmap cho một phương pháp"""
        
        # Prepare data for heatmap
        data = []
        for danger_lv in danger_levels:
            row = [results[danger_lv][tier] for tier in range(self.max_tier + 1)]
            data.append(row)
        
        # Create heatmap
        sns.heatmap(data, 
                   annot=True, 
                   fmt='.1f',
                   cmap='YlOrRd',
                   xticklabels=[f'Tier {i}' for i in range(self.max_tier + 1)],
                   yticklabels=[f'DLv {lv}' for lv in danger_levels],
                   ax=ax,
                   cbar_kws={'label': 'Probability (%)'})
        
        ax.set_title(title, fontweight='bold')
        ax.set_xlabel('Material Tier')
        ax.set_ylabel('Danger Level')
    
    def _plot_comparison(self, old_results, exp_results, log_results, danger_levels, ax):
        """Vẽ biểu đồ so sánh tier trung bình"""
        
        def calculate_avg_tier(results):
            avg_tiers = []
            for danger_lv in danger_levels:
                weighted_sum = sum(tier * prob for tier, prob in results[danger_lv].items())
                avg_tiers.append(weighted_sum / 100)
            return avg_tiers
        
        old_avg = calculate_avg_tier(old_results)
        exp_avg = calculate_avg_tier(exp_results)
        log_avg = calculate_avg_tier(log_results)
        
        ax.plot(danger_levels, old_avg, 'r-o', label='Old Formula', linewidth=2, markersize=6)
        ax.plot(danger_levels, exp_avg, 'b-s', label='New Exponential', linewidth=2, markersize=6)
        ax.plot(danger_levels, log_avg, 'g-^', label='New Logarithmic', linewidth=2, markersize=6)
        
        ax.set_xlabel('Danger Level')
        ax.set_ylabel('Average Tier')
        ax.set_title('Average Tier Comparison', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, self.max_tier)
    
    def _create_statistics_table(self, old_results, exp_results, log_results, danger_levels):
        """Tạo bảng thống kê chi tiết"""
        
        print("\n" + "="*80)
        print("DETAILED TIER DISTRIBUTION STATISTICS")
        print("="*80)
        
        for danger_lv in danger_levels:
            print(f"\nDanger Level {danger_lv} (Effective Level: {danger_lv // 3}):")
            print("-" * 60)
            
            # Create comparison table
            df_data = {
                'Tier': list(range(self.max_tier + 1)),
                'Old Formula (%)': [old_results[danger_lv][tier] for tier in range(self.max_tier + 1)],
                'Exponential (%)': [exp_results[danger_lv][tier] for tier in range(self.max_tier + 1)],
                'Logarithmic (%)': [log_results[danger_lv][tier] for tier in range(self.max_tier + 1)]
            }
            
            df = pd.DataFrame(df_data)
            print(df.to_string(index=False, float_format='%.1f'))
            
            # Calculate average tiers
            old_avg = sum(tier * old_results[danger_lv][tier] for tier in range(self.max_tier + 1)) / 100
            exp_avg = sum(tier * exp_results[danger_lv][tier] for tier in range(self.max_tier + 1)) / 100
            log_avg = sum(tier * log_results[danger_lv][tier] for tier in range(self.max_tier + 1)) / 100
            
            print(f"\nAverage Tiers:")
            print(f"  Old Formula: {old_avg:.2f}")
            print(f"  Exponential: {exp_avg:.2f}")
            print(f"  Logarithmic: {log_avg:.2f}")

def main():
    """Chạy phân tích chính"""
    analyzer = MaterialTierAnalyzer()
    
    # Define danger levels to analyze (TraitShrine uses owner.LV / 3)
    danger_levels = [0,30, 60, 90, 120, 150, 180, 210]  # DLv 10-100 effective
    
    print("Material Tier Distribution Analysis for TraitShrine")
    print(f"Formula: MATERIAL.GetRandomMaterial(owner.LV / 3, material_type)")
    print(f"Analyzing danger levels: {danger_levels}")
    print(f"Samples per level: {analyzer.samples}")
    
    # Create visualization
    analyzer.create_visualization(danger_levels)
    
    print("\nAnalysis complete! Check 'tier_distribution_analysis.png' for visual results.")

if __name__ == "__main__":
    main()
