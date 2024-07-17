# SCvx

<details>
<summary>
    Research Question
</summary>
    How can a <ins>vehicle</ins> find <ins>an</ins> optimized solution in <ins>real-time</ins> for <ins>general situation</ins>?
</details>

## Frame Work
    1. Find a warm start initial value
    2. Optimization

## Work Flow
    Q1. [narrow path를 정확히 통과하는 코드를 작성 + DNN 학습 -> warm start 방법 활용]
        'narrow path를 정확히 통과하는 코드를 작성' 부분은 'hybrid A* 를 통한 경로 설정 -> warm-start에 활용해서 최적화로 path 구하기' 
        최적화는 SCP를 쓰거나 IPOPT 쓰거나 뭐가 좋은지는 둘다 해봐야 알 수 있을거 같네요. 
        뻣어나갈 수 있는 방향은 크게 세가지 아래 방향으로 생각되는데, 이건 하면서 뭐를 더 생각해볼 지 정할 수 있을거 같네요.
        1. 최적화 문제 formulation 개선, 2. 최적화 자체 알고리즘 개선, 3. 실제적용을 위한 문제 셋팅 하에서 구현 코드 작성 (드론, 로보틱스, 자율 주행 등) 
        대표적으로 이와 관련되서 많이 하시는 분 중에 Moritz Diehl 교수님이 계신데, 예를 들어 2304.12908 (arxiv.org) 와 같은 논문도 같이 생각해볼만 합니다. 제가 3과 관련되서는 공대 교수님들과 교류를 좀 해볼 계획입니다. 
    v1. 1. Change obstacles
        2. Introduce hybrid A* for warm-start
        3. Choose Optimization method
        4. DNN
    
### Change obstacles
    Input 1: location type
        1. Random location & radius
        2. Fixed location & radius
    Input 2: Number of obstacles
    Input 3: (Type2) location & radius for fixed obstacles
    