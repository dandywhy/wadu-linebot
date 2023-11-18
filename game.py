def guess_nb(guess, ans):
  guess = [int(g) for g in str(guess)]
  a = 0
  b = len([k for k in ans if k in guess])
  for i, v in enumerate(ans):
    if (guess[i] == v):
        a += 1
  b -= a
  return a, b