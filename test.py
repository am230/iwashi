import iwashi

result = iwashi.visit("https://www.youtube.com/@hololive")
if result:
    iwashi.helper.print_result(result)
