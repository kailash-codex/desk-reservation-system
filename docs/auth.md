# Authentication and Authorization

## Authentication

Authentication in `csxl.unc.edu` is integrated with UNC's Single Sign-on (SSO) Shibboleth service. This allows username, password, and UNC affinity to be handled by UNC ITS and our application takes a dependency upon it. For more information on SSO, see ITS' [official documentation](https://its.unc.edu/2017/07/24/shibboleth/). For the implementation details on *how* authentication works in this application, see [backend/api/authentication.py](backend/api/authentication.py).

Authentication is verifying *who* the "subject" accessing a system is. The term "subject" is chosen intentionally in the security lexicon. A subject may be a person, but alternatively an automated program accessing a system on behalf of a person, group, or organization. The CSXL application is, for now, foremost a user-facing application that serves the people of the computer science department at UNC. Thus, a "subject" is a person and user of the CSXL application for our concerns.

## Authorization

Authorization is verifying a subject/user *has permission* to carry out an *action* on a *resource* within the system. For example, the leader of a workshop may have permission to edit a workshop's details, whereas a registered participant of a workshop would not. Additionally, a site administrator may every permission possible, whereas a newly registered user does not.