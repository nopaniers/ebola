Title: A simple model of the Ebola Virus
Date: 04-09-2014
<style type="text/css">
    .math span {
        color: inherit;
    }
</style>
<script language="javascript">
    if(window.MathJax===undefined){
        var script = document.createElement("script");  
        script.type = "text/javascript";  
    script.src  = "http://cdn.mathjax.org/mathjax/latest/MathJax.js";
        var config = 'MathJax.Hub.Config({' +
                    'extensions: ["tex2jax.js"],' +   
                    'tex2jax: { '+
                      'inlineMath: [ ["$","$"]], '+
                      'displayMath: [["\\[","\\]"]],'+
                      'processEscapes: true '+
                    '},' +
                    'jax: ["input/TeX","output/HTML-CSS"]' +
                    '});' +
                    'MathJax.Hub.Startup.onload();';
        if (window.opera) 
            script.innerHTML = config;
        else
            script.text = config;
        document.getElementsByTagName("head")[0].appendChild(script);
    }
</script>

Ebola virus is spreading in West Africa. This is a simple mathematical model of that. Before we begin, let me say that I am not a doctor. The model, as it stands, is a very simple model and most likely doesn't capture reality. In particular, any change to the number of people each patient infects makes a huge difference to how well the virus spreads. Please give feedback or suggestions for how to make it better.

## The virus

Looking at the data coming out of West Africa, things don't look good. 

![The total (cumulative) number of cases and deaths due to Ebola in West Africa.](http://dl.dropboxusercontent.com/u/77767081/casesdeaths.png)

This graph is simply a plot of the total (cumulative) number of cases and deaths in West Africa. It's on a log-linear plot, so even though the lines look straight, the numbers are growing exponentially. I've fitted a straight line to the numbers since June.

>  Currently the number of cases and deaths due to Ebola doubles every month.

To be more precise, it doubles every 29 days. If nothing happens to change that rate, in nine months we will have one million cases, and two years from now a significant fraction of the world's population will have had the disease. We obviously need a better model than just exponential growth forever, and so this post is a first attempt to provide a simple one.


## The model

There are four main categories of people in this model:

**S** are people who have not contracted the virus yet. Worryingly if they come into contact with someone who is infectious, they might get the disease.

**E** are people who have the disease, but don't yet show the symptoms, and aren't yet infectious.

**I** are people who have full blown Ebola. They're infectious. Their body is a battle with the virus, which they'll either win, or lose.

**R** are people who have won the battle, and have recovered. They are now immune to the disease.

Another useful number to keep track of is the total number of people still alive, which is **N**, and is the sum of all of these.

I modelled these according to some simple coupled differential equations:
	
\[
\begin{align}\frac{dS} {dt} &= -\beta \frac{S}{N} I \\\\
\frac{dE}{dt}  &= +\beta \frac{S}{N} I -\sigma E \\\\
\frac{dI}{dt} &= +\sigma E - \gamma I \\\\
\frac{dR}{dt} &= (1-f) \gamma I
\end{align}
\]Initially I started my model with just one case (E=1), and every other person uninfected (S).


## Explanation of the model

This section gives an explanation of the model and the parameters I chose. If you just want to see the results, feel free to skip it.

The more infectious people there are (*I*) the more people they will infect. Each infectious person has a certain chance per day, which we'll call $\beta$ of giving it to someone else. Someone can only get it if they aren't immune (because they've already had it), $S/N$ is the fraction of people still vulnerable. So from new infections we have,

$$\begin{align}\frac{dS} {dt}  &= -\beta \frac{S}{N} I \\\\
\frac{dE}{dt}   &= +\beta \frac{S}{N} I 
\end{align}
$$
   	
Once a person is infected (E), they take some time to show symptoms and become infectious (I). Some people take more time, some people less, but in previous Ebola outbreaks, they estimated it takes around 5.4 days. We'll model this with a *rate* of going from $E$ to $I$ of $\sigma = 1/5.4$ per day and  
\[\begin{align}\frac{dE}{dt} = -\sigma E \\\\
\frac{dI}{dt} = +\sigma E 
\end{align}
\] 

Once they're infectious, they'll either recover, or die. Again, we'll model this with a *rate* found in previous outbreaks, of $\gamma = 1/5.61$ per day. The faction of these people who die (according to a simple ratio of deaths to cases) is currently estimated by WHO to be 52%. It seems to me that they got this number by simply dividing the number of deaths by the number of cases (because that's what you get if you do that). However, considering several of the current cases will die, it seems reasonable to me that the fatality rate is slightly higher - in my model I made it, $f=63\%$ of people dying, and $1-f=37\%$ of people surviving, which gives the correct ratio of cases to deaths, once the current cases have been taken into account. These considerations give the following two equations,

\[\begin{align}
\frac{dI}{dt} &= - \gamma I \\\\ \frac{dR}{dt} &= (1-f) \gamma I
\end{align}
\] 
   

I didn't yet give a value for $\beta$, the rate that people in the general population get infected. It is an important parameter: the average number of people who an ebola patient could infect is called the "reproduction number" and is given by

\[R_0 = \frac{\beta}{\gamma}]
	
Or, if you take into account that some people are immune, we get the "effective reproduction number", which is the number of people an ebola patient gives ebola of

\[R_e= \frac{S}{N} {\beta}{\gamma}] 

In previous outbreaks, they've estimated $R_0$ to be between 1.3 and 2.7. It makes sense that it could be quite different in different countries and different conditions - it would depend on sanitary conditions, on local customs, and how likely someone was to stay at home, or present to a hospital - and how well equipped the hospitals are once a patient gets there. All of these things have a massive impact on how well the virus spreads. It's no wonder experts are calling for assistance for Ebola ravaged countries, because even a small change has a big impact on the severity of what happens next.

In my model, we'll go for the optimistic end of the range. To match the current rate of increase (doubling every 29 days), I'm going to use a reproduction number of $R_0=1.29$.

	
## ResultsI solved this system of differential equations numerically using odeint in Python. The (simple) code to do so is online [here](http://github.com/nopaniers/ebola). Feel free to modify, improve or use it however you like.

First, let's show that we can reproduce similar numbers to what we're seeing right now in West Africa.

![Model predictions (shown as solid lines) against the actual numbers reported, shown as points](http://dl.dropboxusercontent.com/u/77767081/earlyprediction.png)

As you can see, the model doesn't match well for the early numbers, before May, but once the exponential growth phase takes off the agreement seems to be pretty good. We're definitely capturing the rate of increase, the ratio between cases and deaths.

So what does the future hold? I ran my model (rather arbitrarily) assuming a hypothetical total population of 1 million people.The numbers of infected people continues to grow exponentially, until a substantial proportion of the population has already been infected (and is therefore resistant). When this happens, it's less likely that the disease will spread, and the average reproduction number drops below 1. This happens in the first half of next year. At this point, the numbers of patients drops begin to drop. Eventually the disease subsides. At that point over half the population have had Ebola, and over 400,000 people are dead.

![Predictions for a hypothetical nation of one million people, showing the model's numbers for S, E, I, R, as well as deaths, D.](http://dl.dropboxusercontent.com/u/77767081/million.png)

What if Ebola just continued spreading in the rest of the world, the way that it has been spreading through West Africa? What happens if we bump up the model to include 7 billion people, but keep all the rest of the parameters the same? A similar thing happens to hypothetical million person country. It continues growing for much longer and the numbers of diseased and dead are far higher (three billion dead with four billion survivors, half of whom recovered from Ebola, and half who were lucky enough never to get it).

![Model assuming Ebola spreads worldwide with similar parameters to what we have seen in West Africa, showing the model's numbers for S, E, I, R, as well as deaths, D.](http://dl.dropboxusercontent.com/u/77767081/world.png)

Finally, what would happen for the next year, given the parameters don't change much? Because most of the world's population hasn't been infected with Ebola yet, there's no resistance to it, and the model just shows exponential growth for the foreseeable future. If this happens, by this time next year there will have been some twenty million deaths due to Ebola.

![Model assuming Ebola spreads worldwide with similar parameters to what we have seen in West Africa, for the next year showing the model's numbers for S, E, I, R, as well as deaths, D.](http://dl.dropboxusercontent.com/u/77767081/year.png)

Thanks to [jf22](http://www.reddit.com/user/jf22) from reddit, who suggested that $\beta$ decaying by 1% per day would make a big difference. It does. If that happens then Ebola is stopped in its tracks, and the "the world is saved". Less than 7,000 people die. It's clear that if we can reduce this rate it has a drastic impact on how Ebola spreads, the question is - how do we do it in reality, and how do we model that?

![Model assuming that the transmission rate drops 1% per day from the beginning of September 2014.](http://dl.dropboxusercontent.com/u/77767081/decay.png)

