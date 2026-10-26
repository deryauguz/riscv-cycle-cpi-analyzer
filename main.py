import re
from collections import Counter

class RISCVPerformanceAnalyzer:
    def __init__(self):
        # Maliyet tablosu (Cycle Costs)
        self.cycle_costs = {
            'ALU': 1,      # add, sub, addi, and, or, xor vb. (1 Cycle)
            'LOAD': 4,     # lw, lh, lb vb. (4 Cycle)
            'STORE': 4,    # sw, sh, sb vb. (4 Cycle)
            'BRANCH': 3,   # beq, bne, blt vb. (3 Cycle)
            'JUMP': 3,     # jal, jalr (3 Cycle)
            'OTHER': 1
        }
        
        # İstatistik Takibi
        self.total_instructions = 0
        self.type_counts = Counter()
        self.opcode_counts = Counter()
        self.instruction_log = []

    def classify_instruction(self, opcode: str) -> str:
        opcode = opcode.lower()
        if opcode in ['add', 'sub', 'and', 'or', 'xor', 'sll', 'srl', 'sra', 
                      'addi', 'andi', 'ori', 'xori', 'slli', 'srli', 'srai', 
                      'lui', 'auipc', 'slt', 'slti', 'sltu', 'sltiu']:
            return 'ALU'
        elif opcode in ['lw', 'lh', 'lb', 'lbu', 'lhu']:
            return 'LOAD'
        elif opcode in ['sw', 'sh', 'sb']:
            return 'STORE'
        elif opcode in ['beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu']:
            return 'BRANCH'
        elif opcode in ['jal', 'jalr']:
            return 'JUMP'
        return 'OTHER'

    def parse_line(self, line: str):
        clean_line = line.split('#')[0].split(';')[0].strip()
        if not clean_line:
            return

        if ':' in clean_line:
            clean_line = clean_line.split(':')[-1].strip()
            if not clean_line:
                return

        tokens = re.findall(r'[a-zA-Z]+', clean_line)
        if tokens:
            opcode = tokens[0].lower()
            category = self.classify_instruction(opcode)
            cost = self.cycle_costs[category]

            self.total_instructions += 1
            self.opcode_counts[opcode] += 1
            self.type_counts[category] += 1
            
            self.instruction_log.append({
                'line': clean_line,
                'opcode': opcode,
                'category': category,
                'cost': cost
            })

    def calculate_total_cycles(self) -> int:
        total_cycles = 0
        for category, count in self.type_counts.items():
            total_cycles += count * self.cycle_costs[category]
        return total_cycles

    def generate_report(self):
        if self.total_instructions == 0:
            print("Uyarı: İşlenecek geçerli bir RISC-V komutu bulunamadı!")
            return

        total_cycles = self.calculate_total_cycles()
        cpi = total_cycles / self.total_instructions

        print("=" * 65)
        print("          RISC-V PERFORMANS VE MALİYET ANALİZ RAPORU")
        print("=" * 65)
        print(f"Toplam Komut Sayısı (Instruction Count) : {self.total_instructions}")
        print(f"Toplam Hesaplanan Maliyet (Total Cycles): {total_cycles} Cycle")
        print(f"Ortalama Komut Başına Döngü (CPI)      : {cpi:.2f}")
        print("-" * 65)
        
        print("\n[1] KOMUT GRUBU MALİYET DAĞILIMI:")
        print(f"{'Kategori':<10} | {'Birim Maliyet':<14} | {'Komut Adedi':<12} | {'Toplam Maliyet (Cycle)'}")
        print("-" * 65)
        for cat in ['ALU', 'LOAD', 'STORE', 'BRANCH', 'JUMP', 'OTHER']:
            count = self.type_counts[cat]
            if count > 0:
                unit_cost = self.cycle_costs[cat]
                cat_total = count * unit_cost
                print(f"{cat:<10} | {unit_cost:<14} | {count:<12} | {cat_total}")

        print("\n[2] AYRINTILI KOMUT İZLEME (TRACE LOG):")
        print(f"{'Satır/Komut':<30} | {'Grubu':<8} | {'Maliyet'}")
        print("-" * 50)
        for item in self.instruction_log:
            print(f"{item['line']:<30} | {item['category']:<8} | {item['cost']} Cycle")

        print("=" * 65)


if __name__ == "__main__":
    # Analiz edilecek RISC-V montaj kodları (Doğrudan Python içinde tanımlı)
    riscv_code = """
    addi x5, x0, 5       # ALU (1 Cycle)
    addi x6, x0, 10      # ALU (1 Cycle)
    add  x7, x5, x6      # ALU (1 Cycle)
    lw   x10, 0(x5)      # LOAD (4 Cycle)
    lw   x11, 4(x5)      # LOAD (4 Cycle)
    sw   x10, 0(x6)      # STORE (4 Cycle)
    beq  x5, x6, 12      # BRANCH (3 Cycle)
    jal  x1, 100         # JUMP (3 Cycle)
    sub  x7, x7, x5      # ALU (1 Cycle)
    """

    analyzer = RISCVPerformanceAnalyzer()

    # Kod satırlarını oku ve analiz et
    for line in riscv_code.strip().split('\n'):
        analyzer.parse_line(line)

    # Raporu bas
    analyzer.generate_report()