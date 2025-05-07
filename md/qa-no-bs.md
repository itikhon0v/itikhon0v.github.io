Applied QA: How not to drown
2025-05-06
web, qa, getting-things-done

# Why this guide exists

When I started working in the web development, one of my first jobs in our small company was to QA the websites we built. At the time I knew almost nothing about testing, and I found the QA resources online totally unhelpful: it was all either hardcore bloated theory, or automation docs, both free and paid courses.

This really made my path in testing slow, and mostly very frustrating. I constantly wondered if I was missing something or doing it wrong. So I decided to review my past experience, and make an actual introduction to manual testing without buzzwords and pack it with useful links and notions.

Some of this might seem naive or simple, but honestly, it is better to start _doing and learning_ than to scrolling those endless articles.

# 1. Set Standards Before You Test

Before we evaluate that a piece of software, like an app, or a website is ready to go in the production, we need to define our passing criteria:

Before you say something is "done", you need to know what _done_ means.

## Read the Ticket (Even If It's a Mess)

In some small teams, and honestly, even in big ones this part can be challenging: Development ticket might feel more like a stream of consciousness, and it would be hard to even skim through it. But even if it is a very vague, ambiguous, or just a lazy scribble, it is still one of the most important parts in the QA process.

If it doesn't have exact passing criteria, try to note the most important points from it, just to have a more convenient check list to look at while testing. Also some things might be missed, like internal rules or habits how your team ships the software. If you're an experienced part of the team, you know them, but still, it is a very good practice to write them down in that list as well.

## Don't Ignore Accessibility

If your project will be used by the public, accessibility isn’t optional. Standards like ADA, WCAG (my favorite), or local equivalents are essential.

But don't worry, you don't have to read them cover to cover. Here are quick points from [WCAG 2.1](https://www.w3.org/TR/WCAG21/):

- Keyboard-Only Navigation ([WCAG 2.1.1 - Keyboard](https://www.w3.org/TR/WCAG21/#keyboard))
- Font Size Respects Zoom ([WCAG 1.4.4 - Resize Text](https://www.w3.org/TR/WCAG21/#resize-text))
- Good Color Contrast ([WCAG 1.4.3 - Contrast(minimum)](https://www.w3.org/TR/WCAG21/#contrast-minimum))
- Elements Are Properly Labeled ([WCAG 1.1.1 - Non-text Content](https://www.w3.org/TR/WCAG21/#non-text-content))
- Responsive Layout ([WCAG 1.4.10 - Reflow](https://www.w3.org/TR/WCAG21/#reflow))
- Use Real Elements ([WCAG 1.3.1 - Info and Relationships](https://www.w3.org/TR/WCAG21/#info-and-relationships))

There are many very important concepts. If you haven't read WCAG standards, please consider looking into, it will make you a better developer and a tester.

# 2. Use Tools That Actually Help

Another big point in the IT industry - know your tools. There are many very nice tools for checking accessibility and overall site performance/security state, I will not list them all, but here is a handy list for all sorts of tests:

## Core Tools

- Notes

Use anything: Text Editor or Paper. What is important is to keep your checklist there, write down your observations and thoughts. Don't trust your brain mid-session.

- Screen Recording Tool

Anything that lets you quickly:

- Take screenshots
- Record short clips
- Annotate them with shapes and text

## Browsers

Not many beginners know, there aren't many browsers in the wild, basically, most of the market can be divided into 3 browser engines:

- Chromium (Chrome, Edge, Brave)
- Gecko (Firefox)
- WebKit (Safari, GNOME Web)

Test core flows in each, and you can be sure, that you're covering most real-world users.

## DevTools

This is where 80% of your bug-hunting happens:

- Inspect elements, layout, and spacing
- Check console for JS errors/warnings
- Use **device emulation** to test responsiveness
- Watch network requests and load times
- Set breakpoints to debug JS

Bonus Habit: Don't Be Afraid to Read the Code

You don't have to be a developer to look at source code. Reading the function code will save you hours of guesswork, and might be especially helpful when you deal with regexes.

## Accessibilty + Markup Checkers

- WAVE ([site](https://wave.webaim.org/)/[extension](https://wave.webaim.org/extension/))
  Beginner-friendly accessibility checker. Great for finding missing alt tags, checking contrast and unlabeled inputs
- Lighthouse (built into Chrome)
  Run quick audits for accessibility, performance and SEO. Exportable as PDF
- W3C HTML Validator ([link](https://validator.w3.org/))
  Timeless classics.

## Cross-Device Testing

- BrowserStack
  Test your site on different devices, screen sizes, OSes without owning 15 phones. Use it for layout and compatibility checks after DevTools.

## Important Note

You don't have to install all of them right now. They're good, but only for their purpose. Try, but do not forget that there is no silver bullet for all the bugs.

# 3. Break Things on Purpose (and With Purpose)

This is the part that had me stuck for a while.

I used to think QA meant following test cases. Like, one day I’d take a course, read a book, and finally unlock the mystical _list of test scenarios._ But the short answer is:

**Tuesday.**

Or `alert("This site has just been XSSed!")`.

Users don’t follow rules. So why should you?

If there is an input field - _break it_.

If there's a flow - _interrupt it halfway_.

Your job isn't to verify - it is to experiment, to **fuck around**, to _unleash your inner gremlin with a keyboard._

Of course, test cases are important. But in many situations, it is impossible (or unrealistic) to define every possible test case for every possible flow. Over time you will build your own library: patterns that come up often, the things no one remembers to test until it is live.

But if you don't know where to start, here is your **professional Gremlin Starter Pack:**

## Edge Case Hunting

I usually keep a handy folder with some niceties:

- **A 1000 word epos** about [Lorem Ipsum](https://www.lipsum.com/). Great for overflowing small fields or testing scroll behavior.
- UTF8 stress test: [This Russian 4chan-style pasta about fried soup](https://neolurk.org/wiki/%D0%A1%D1%82%D0%B0%D1%80%D0%B0%D1%8F_%D0%BA%D0%BE%D0%BF%D0%B8%D0%BF%D0%B0%D1%81%D1%82%D0%B0:%D0%96%D0%B0%D1%80%D0%B5%D0%BD%D1%8B%D0%B9_%D1%81%D1%83%D0%BF#%D0%9E%D1%80%D0%B8%D0%B3%D0%B8%D0%BD%D0%B0%D0%BB)
- **Massive PNG file**: To test file size restrictions on uploads. I generate one like this:

```python
from PIL import Image
import numpy as np
import os

def big_boy(path, target_mb=1):
    estimated_bytes_per_pixel = 2.5
    target_bytes = int(target_mb * 1024 * 1024)
    total_pixels = int(target_bytes / estimated_bytes_per_pixel)
    side = int(total_pixels ** 0.5)

    array = np.random.randint(0, 256, (side, side, 3), dtype=np.uint8)
    image = Image.fromarray(array, 'RGB')

    image.save(path, format='PNG', optimize=False, compress_level=0)

    actual_size = os.path.getsize(path) / (1024 * 1024)
    print(f"Saved image at '{path}' with size: {actual_size:.2f} MB (target: {target_mb} MB)")

big_boy(path="image.png", target_mb=200)
```

- A couple of SQL and NoSQL injections: `; DROP TABLE users;--` and `{ "&ne": null }` are more than enough
- Emojis
- Or just leave those fields empty and hit "Submit" - You'd be amazed.
- Bonus: Learn how phone numbers, emails, and zip codes are usually formatted. Try to break their regex. Later, your devs will thank you for saving them from a DB full of broken data.

## Structured Chaos

This part is about simulating accidental chaos: tabbing away, hitting refresh, doing things users might do without thinking.
Things to try:

- Mid-flow refresh
- Go back and forward
- Use VPN
- Turn off JavaScript and reload
- Open the same flow in two tabs
- Throttle your network in DevTools
- Disconnect from the internet
- Clear your cookies/localStorage

These aren't "edge cases", but more like real things real users do. This is almost a stress test for your site.

## Persona Testing

Not everyone uses internet the same way. Time to act as:

- Senior user with zoomed-in fonts on an iPad.
- Someone with a very small screen and slow internet
- A keayboard-only user
- A minor
- A screen reader user

You don't need a full accessibility setup. Just try different masks, look from different perspectives on the site, run VoiceOver/Narrator, zoom in, act differently

# 4. Document Bugs Clearly (and Kindly)

You broke it. Nice.

Now comes the part where you tell someone - _without making them hate you._

Bug reporting isn’t a "gotcha" moment. It is not a dev's failure and your win. You're not pointing fingers - you're catching things early so the whole team (and company) doesn't lose credibility later.

Think of yourself as a **safety net**. You're helping everyone look better - and your bug report is part of that process. Here's how to do it well, and do it kindly.

## Include Attachments

Every bug report should ideally have:

- Screenshots - clear and cropped
- Screen recordings - especially for anything animated or hard to explain
- Clear reproduction steps - written out step-by-step
- Expected vs Actual behavior
- Console/Network logs

## Be Kind (and Precise)

A good QA report is always:

- Friendly - use a nice tone
- Precise - don't be vague
- Helpful - you can suggest, but do not dictate

Instead of:

> This button is broken

Use:

> Clicking 'Save' shows a success message, but the data isn't stored (see Network tab -> 500 on error on `/save`)

## Suggest Improvements

This is an underrated part of QA. You're not just finding what's broken - you are often the **last line of sanity** before the real world sees the product.

Imagine it is a hackathon. You built the next TikTok, but forgot the sign-up form.

So if you notice something small that could be better - **say so**

- Font size is a bit tight on mobile - maybe bump it up to 14px?
- This animation is too fast to read - could use 300ms or more

QA isn't a race between you and the devs. You're their **best friend** and their **worst nightmare** - but only because you see the things they will regret after launch, before anyone else does.

# 5. Automate When (and Only When) It's Worth It

I'll be honest. Most of the time I do not automate tests.

Our projects are small, fast, and temporary, meaning that by the time you write a _robust test suite_, the site will be **gone**. I am not saying that tests are useless, because they're very important. Just don't try to cover all 100% of the code base, use strategic mind and still keep some part of your QA manual (remember: QA is not only about ticking off checkboxes, but is also a **sanity check**)

If I were to recommend something where to start doing automation, I would recommend [Playwright](https://playwright.dev/):

- Cross-browser testing (you can even do WebKit on Windows)
- Records your user actions directly into test code

Personally I’ve found that it’s faster and easier to work with compared to Selenium.

# 6. Know When to Stop

You won’t catch everything. And that's okay.

One of the hardest parts of QA is learning when **enough is enough**. IT is an eternal rabbit hole, especially in QA - where total number of permutations of all devices/actions/conditions *tends to infinity*. But your job isn’t to achieve perfection. It’s to protect the user from the obvious, the sloppy, and the phantasmagoric failures.

A good rule of thumb:

> When you're tired, take a break.
> Come back fresh. Do a final loop, and call it a day.

This is not giving up - it is being realistic. Your QA report doesn't have to be complete, it has to be **useful**.

**Pro tip**: If possible, setup multiple QA testers, especially from different backgrounds. The more eyes on your product, the better your real-world coverage.

# Sample QA Routine

Now when I wrote so much about different testing tools, techniques, even mindset, let's play a game:

## Development Ticket: Sweepstakes Entry Form

### Description:

Create a basic form where users can enter their email address to join our monthly sweepstakes.

- Campaign runs for 3 months
- One entry per email per month
- On success show "Thank You" page
- On repeat submission show "Already Entered" page

*Attached*: Mockup, Images, Fonts, Copy text

The ticket is almost like I said in the first section, just cleaner (sometimes you even have to read it a few times before gettings something like the list above). But we are still missing acceptance criteria, no validation rules, no browser/device targets. So here's kind of a checklist I’d write after reading the ticket and thinking it through for 2 minutes:

## QA Checklist

<label>
  <input type="checkbox">
  Form renders correctly on homepage
</label><br>
<label>
  <input type="checkbox">
  Run WAVE test
</label><br>
<label>
  <input type="checkbox">
  Submit empty form, see if there are any error messages
</label><br>
<label>
  <input type="checkbox">
  Submit incorrect data to check email mask
</label><br>
<label>
  <input type="checkbox">
  Submit correct email, see if return matches with the ticket
</label><br>
<label>
  <input type="checkbox">
  Submit previous email, see if return matches with the ticket
</label><br>
<label>
  <input type="checkbox">
  Change your record in the DB to last month and submit previous email
</label><br>
<label>
  <input type="checkbox">
  Can navigate using only keyboard
</label><br>
<label>
  <input type="checkbox">
  Is it responsive?
</label><br>
<label>
  <input type="checkbox">
  Scale up to 200%
</label><br>
<label>
  <input type="checkbox">
  Does it work on other devices?
</label><br>

I know this checklist is not perfect or complete. But neither was the ticket, so I have to fill the gaps, make some assumptions, and test what feels important. It is what it is.

# Final Words

QA is a mindset. Be curious, stay chaotic, ask questions no one else thought to ask, and always look at the product like a real user would.

You don't need to be perfect, and you definitely don’t need to catch every bug. What matters is **impact** - the difference you make by noticing what others missed, and by speaking up before it’s too late.
