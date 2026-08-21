# Reviewer Resources

Covers: what reviewers check, reviewer tools, and how to volunteer to review. Doubles as an author-facing "what the reviewer will look for" checklist.

## Chapter - Reviewer Resources Overview

- Reviews are public: every submission review happens in the open on the `Bioconductor/BiocContributions` GitHub issue tracker.
- Anyone in the community may comment on any review, not just the assigned reviewer.
- All feedback must follow the Bioconductor Code of Conduct.
- Three resources make up this section: review expectations (what/how to review), reviewer tools (checklist + examples), and volunteer sign-up.

## Chapter 31 - Review Expectations

Who reviews and the commitment:

- Reviewers must maintain at least one active Bioconductor package.
- Budget roughly 30 minutes to 1.5 hours per package review.
- Complete the review within 3 weeks of assignment.

What reviewers evaluate (author-facing checklist of focus areas):

- Ease of use of the package (intuitive API, sensible defaults).
- Documentation quality: complete man pages, a runnable vignette, clear examples.
- Well-written code: readable, maintainable, follows Bioconductor coding style.
- Interoperability: reuse of core Bioconductor classes and infrastructure rather than reinventing them.

Note: Chapter 31 sets the process and focus areas. The detailed, item-by-item checklist lives in the reviewer tools chapter (below) and in the package development guidelines chapters.

## Chapter 32 - Reviewer Tools

- Package Review Checklist: a ready-made template reviewers paste into the relevant New Submission Tracker issue and tick off / update as the review proceeds.
- New Submission Tracker: the `Bioconductor/BiocContributions` GitHub issues are where reviews are conducted and the checklist is posted and tracked over time.
- Example reviews: completed reviews (e.g. MAGAR, HubPub, BiocSet) are linked as references for the expected standard and tone.
- The checklist plus automated `BiocCheck` / `R CMD check` output from the Single Package Builder drive the concrete pass/fail items an author must resolve.

Authors: expect the reviewer to walk this checklist publicly in your submission issue, so pre-run `BiocCheck` and clear ERRORs/WARNINGs before requesting review.

## Chapter 33 - Volunteer to Review

- Anyone in the community can volunteer as a Bioconductor community reviewer; no special credentials required.
- Before signing up: read the Review Expectations chapter and the Bioconductor Code of Conduct.
- Sign up via the volunteer Google form (linked from the chapter).
- Volunteers are then assigned incoming packages from the New Submission Tracker.

Source: [Reviewer resources overview](https://contributions.bioconductor.org/reviewer-resources-overview.html) , [Review expectations](https://contributions.bioconductor.org/review-expectation.html) , [Reviewer tools](https://contributions.bioconductor.org/reviewtools.html) , [Volunteering to review](https://contributions.bioconductor.org/review-volunteer-chapter.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
