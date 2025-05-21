"""
Tests de Kolmogorov-Smirnov y Chi-Cuadrado para las distribuciones indicadadas en el enunciado
K-S: Uniforme, Exponencial, Normal
Chi-Cuadrado: Binomial, Poisson, Empírica Discreta
"""
from distribuciones import uniforme, exponencial, normal, binomial, poisson, empirica_discreta
from scipy.stats import kstest, chisquare, binom, poisson as poisson_dist
from collections import Counter

def generate_samples(distribution, params, n=5000):
  if distribution == 'uniforme':
    return [uniforme(*params) for _ in range(n)]
  elif distribution == 'exponencial':
    return [exponencial(params[0]) for _ in range(n)]
  elif distribution == 'normal':
    return [normal(params[0], params[1]) for _ in range(n)]
  elif distribution == 'binomial':
    return [binomial(params[0], params[1]) for _ in range(n)]
  elif distribution == 'poisson':
    return [poisson(params[0]) for _ in range(n)]
  elif distribution == 'empirica_discreta':
    return [empirica_discreta(params[0], params[1]) for _ in range(n)]
  else:
    raise ValueError("Distribución invalida")

def test_uniform(a, b, n=5000):
  sample = generate_samples('uniforme', (a, b), n)

  normalized_sample = [(x - a) / (b - a) for x in sample]

  statistic, p_value = kstest(normalized_sample, 'uniform')

  result = "OK" if p_value > 0.05 else "ERROR"
  print(f"{'Uniforme':<20} {result:<7} — D = {statistic:>7.4f}, p = {p_value:>7.4f}")

def test_exponential(alfa, n=5000):
  sample = generate_samples('exponencial', (alfa,), n)

  statistic, p_value = kstest(sample, 'expon', args=(0, alfa))

  result = "OK" if p_value > 0.05 else "ERROR"
  print(f"{'Exponencial':<20} {result:<7} — D = {statistic:>7.4f}, p = {p_value:>7.4f}")

def test_normal(ex, stdx, n=5000):
  sample = generate_samples('normal', (ex, stdx), n)

  statistic, p_value = kstest(sample, 'norm', args=(ex, stdx))

  result = "OK" if p_value > 0.05 else "ERROR"
  print(f"{'Normal':<20} {result:<7} — D = {statistic:>7.4f}, p = {p_value:>7.4f}")

def test_binomial(n, p, num=5000):
  samples = generate_samples('binomial', (n, p), num)

  observed_counts = Counter(samples)

  k_values = list(range(n + 1))
  observed = [observed_counts.get(k, 0) for k in k_values]

  expected = [binom.pmf(k, n, p) * num for k in k_values]

  statistic, p_value = chisquare(f_obs=observed, f_exp=expected)

  result = "OK" if p_value > 0.05 else "ERROR"
  print(f"{'Binomial':<20} {result:<6} | χ² = {statistic:>7.4f}, p = {p_value:>7.4f}")

def test_poisson(lam, num=5000):
  samples = generate_samples('poisson', (lam,), num)

  observed_counts = Counter(samples)

  k_values = sorted(observed_counts.keys())
  observed = [observed_counts.get(k, 0) for k in k_values]
  expected = [poisson_dist.pmf(k, lam) * num for k in k_values]

  while any(e < 5 for e in expected):
    expected[-2] += expected[-1]
    observed[-2] += observed[-1]
    expected.pop()
    observed.pop()

  total_observed = sum(observed)
  total_expected = sum(expected)
  expected = [e * (total_observed / total_expected) for e in expected]

  statistic, p_value = chisquare(f_obs=observed, f_exp=expected)

  result = "OK" if p_value > 0.05 else "ERROR"
  print(f"{'Poisson':<20} {result:<6} | χ² = {statistic:>7.4f}, p = {p_value:>7.4f}")

def test_empirica_discreta(values, probabilities, num=5000, min_expected=5):
  samples = generate_samples('empirica_discreta', (values, probabilities), num)
  
  observed = [Counter(samples).get(v, 0) for v in values]
  expected = [p * num for p in probabilities]

  grouped = []
  temp_obs = temp_exp = 0
  for o, e in zip(observed, expected):
    temp_obs += o
    temp_exp += e
    if temp_exp >= min_expected:
      grouped.append((temp_obs, temp_exp))
      temp_obs = temp_exp = 0
  if temp_exp > 0:
    if grouped:
      grouped[-1] = (grouped[-1][0] + temp_obs, grouped[-1][1] + temp_exp)
    else:
      grouped.append((temp_obs, temp_exp))

  final_observed, final_expected = zip(*grouped)
  
  statistic, p = chisquare(f_obs=final_observed, f_exp=final_expected)

  result = "OK" if p > 0.05 else "ERROR"
  print(f"{'Empirica Discreta':<20} {result:<6} | χ² = {statistic:>7.4f}, p = {p:>7.4f}")

if __name__ == "__main__":
  print("Resultados de los tests:")
  test_uniform(0, 1, 5000)
  test_exponential(1.5, 5000)
  test_normal(0, 1, 5000)
  test_binomial(n=10, p=0.3)
  test_poisson(lam=4)
  test_empirica_discreta([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
