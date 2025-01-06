// JavaScript source code

// gets list of all swiss german phrases
// TODO get translations, pair them
//[...document.querySelectorAll('b.sc-hHOBVR.jnovYm')].map(elm => elm.innerHTML.trim().replace(/[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~…]/g, "")).filter(a => a != "")

//Does it!!!!
// TODO seperate sentences on same line using puncuation like
// What color do you want? Blue maybe?
// into "What color do you want?" "Blue maybe?"
[...document.querySelectorAll('b.sc-hHOBVR.jnovYm')]
    .filter(elm => elm.innerHTML.trim() != '')
    //.map(elm => [elm.innerHTML.trim().replace(/[!.;]/g, "\n").split('\n')])
    .map(elm => {
        return {
            'phrase': elm.innerHTML.trim().replace(/[?.;!"#$%&()*+,-./:;<=>?@[\]^_`{|}~]/g, ""),
            'translation': (elm.nextSibling.data || '').trim(),
            'phrase-original': elm.innerHTML.trim()
        }
    })
    .filter(elm => elm.phrase != '' && elm.translation != '')
    //.reduce((acc, elm) => {
    //    elm.innerHTML.trim().replace(/[!.;]/g, "\n").split('\n')
    //        .forEach(a => acc.push(a))
    //    return acc
    //}, [])
    //.filter(elm => elm.trim() != '')