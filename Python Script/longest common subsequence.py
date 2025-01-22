str1 = "axbzce"
str2 = "abxzcf"

m = len(str1)
n = len(str2)

dp = [[""] * (n + 1) for _ in range(m + 1)]


for i in range(1, m + 1):
    for j in range(1, n + 1):
        if str1[i-1] == str2[j-1]:
            dp[i][j] = dp[i-1][j-1]+str1[i-1]

        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1], key=len)


print(dp[m][n])
