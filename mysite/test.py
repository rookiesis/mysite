# 평균: 데이터의 기준치(데이터의 쏠림 확인 가능)
# 표준 편차: 분산의 제곱근(데이터의 범주 확인 가능)
# 표준 편차의 3범위 내를 벗어나는 데이터는 이상치 데이터로 판단 가능

# 데이터 입력
scores = [
82, 76, 90, 65, 88, 70, 92, 85, 78, 80,
74, 68, 95, 89, 72, 66, 84, 77, 91, 79,
73, 75, 83, 87, 94, 81, 67, 71, 69, 93
]

# 초기값을 설정하는 생성자 설정
class NormalDistributionAnalyzer:
    def __init__(self, data):
        # 데이터 입력
        self.data = data
        # 평균, 분산을 구하기 위한 데이터의 개수
        self.n = len(data)
        # 평균값, 분산, 표준편차 변수 초기화
        # _를 붙이면 캐시변수이며, 처음 계산한 뒤 재사용하여 중복 연산을 막음
        self._mean = None
        self._variance = None
        self._std = None
    
    # 평균 함수
    def mean(self):
        if self._mean == None:
            self._mean = sum(self.data) / self.n
        return self._mean
    
    # 분산 함수
    def variance(self):
        if self._variance == None:
            m = self.mean()
            self._variance = sum((x - m) ** 2 for x in self.data) / self.n
        return self._variance
    
    # 분산의 제곱근, 표준편차 함수
    def std(self):
        if self._std == None:
            self._std = self.variance() ** 0.5
        return self._std
    
    # 범위 함수
    # k에는 1, 2, 3 값이 들어올 예정
    def within_range(self, k):
        m = self.mean()
        s = self.std()

        # 평균 - k * 표준편차
        lower = m - k * s
        upper = m + k * s

        count = len([x for x in self.data if lower <= x <= upper])
        return round(count / self.n * 100, 1)
    
    # 요약 함수
    def summary(self):
        m = self.mean()
        s = self.std()
        print(f"평균: {m:2f}")
        print(f"표준편차: { s:2f}\n")
        print("표준편차 범위별 데이터 비율")
        print("-------------------------")
        for k in [1, 2, 3]:
            ratio = self.within_range(k)
            print(f"±{k}σ: {ratio}%")

if __name__ == "__main__":
    analyzer = NormalDistributionAnalyzer(scores)
    analyzer.summary()