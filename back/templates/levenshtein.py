def levenshteinDistance(word1, word2):
    N, M = len(word1), len(word2)
    # Create an array of size NxM
    dp = [[0 for i in range(M + 1)] for j in range(N + 1)]

    # Fill 01234... to array
    for j in range(M + 1):
        dp[0][j] = j
    for i in range(N + 1):
        dp[i][0] = i
   
    # Transitions
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j], # Insertion
                    dp[i][j-1], # Deletion
                    dp[i-1][j-1] # Replacement
                )
    return dp[N][M]