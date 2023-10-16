import iwashi

result = iwashi.visit("https://www.reddit.com/user/newfangledgames/")
if result:
    iwashi.helper.print_result(result)
