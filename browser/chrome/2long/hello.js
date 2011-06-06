            function constructUrl(url) {
                return "http://2long.ru/?url=" + url
            }

            function copyToClipboard(text) {
                var input = document.getElementById('url');
                if(input == undefined) {
                    return;
                }
                input.value = text;
                input.select();
                document.execCommand('copy', false, null);
            }

            function showNewUrl() {
                chrome.windows.getCurrent(function(w) {
                    wid = w.id;
                    chrome.tabs.getSelected(wid, function(t) {
                        var newurl = t.url;
                        if (newurl != '') {
                            var req = new XMLHttpRequest();
                            req.open('GET', constructUrl(newurl), true);
                            req.onload = function() {
                                var response = req.responseText;
                                if (response.substr(0, 7) == 'http://') {
                                    document.getElementById('url').innerHTML = "Your url (in clipboard): " + response;
                                    copyToClipboard(response);
                                } else {
                                    document.getElementById('error').innerHTML = "Something wrong"
                                }
                            };
                            req.send(null);
                        }
                    });
                });
            }

            showNewUrl();
