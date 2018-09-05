Simple Mail Transfer Protocol

August 1982: https://tools.ietf.org/html/rfc821
April 2001: https://tools.ietf.org/html/rfc2821
October 2008: https://tools.ietf.org/html/rfc5321

4. The SMTP Specifications
4.1 SMTP Commands
4.2 SMTP Replies

4.2.3  Reply Codes in Numeric Order

  211 System status, or system help reply
  214 Help message (Information on how to use the receiver or the meaning of a particular non-standard command; this reply is useful only to the human user)
  220 <domain> Service ready
  221 <domain> Service closing transmission channel
  250 Requested mail action okay, completed
  251 User not local; will forward to <forward-path> (See section 3.4)
  252 Cannot VRFY user, but will accept message and attempt delivery (See section 3.5.3)
  354 Start mail input; end with <CRLF>.<CRLF>
  421 <domain> Service not available, closing transmission channel (This may be a reply to any command if the service knows it must shut down)
  450 Requested mail action not taken: mailbox unavailable (e.g., mailbox busy)
  451 Requested action aborted: local error in processing
  452 Requested action not taken: insufficient system storage
  500 Syntax error, command unrecognized (This may include errors such as command line too long)
  501 Syntax error in parameters or arguments
  502 Command not implemented (see section 4.2.4)
  503 Bad sequence of commands
  504 Command parameter not implemented
  550 Requested action not taken: mailbox unavailable (e.g., mailbox not found, no access, or command rejected for policy reasons)
  551 User not local; please try <forward-path> (See section 3.4)
  552 Requested mail action aborted: exceeded storage allocation
  553 Requested action not taken: mailbox name not allowed (e.g., mailbox syntax incorrect)
  554 Transaction failed  (Or, in the case of a connection-opening response, "No SMTP service here")

4.3.2 Command-Reply Sequences

  Specific sequences are:

    CONNECTION ESTABLISHMENT
      S: 220
      E: 554
    EHLO or HELO
      S: 250
      E: 504, 550
    MAIL
      S: 250
      E: 552, 451, 452, 550, 553, 503
    RCPT
      S: 250, 251 (but see section 3.4 for discussion of 251 and 551)
      E: 550, 551, 552, 553, 450, 451, 452, 503, 550
    DATA
      I: 354 -> data -> S: 250
                        E: 552, 554, 451, 452
      E: 451, 554, 503
    RSET
      S: 250
    VRFY
      S: 250, 251, 252
      E: 550, 551, 553, 502, 504
    EXPN
      S: 250, 252
      E: 550, 500, 502, 504
    HELP
      S: 211, 214
      E: 502, 504
    NOOP
      S: 250
    QUIT
      S: 221

4.5 Additional Implementation Issues

4.5.1 Minimum Implementation

  In order to make SMTP workable, the following minimum implementation
  is required for all receivers.  The following commands MUST be
  supported to conform to this specification:

    EHLO
    HELO
    MAIL
    RCPT
    DATA
    RSET
    NOOP
    QUIT
    VRFY

4.5.2 Transparency

  Without some provision for data transparency, the character sequence
  "<CRLF>.<CRLF>" ends the mail text and cannot be sent by the user.
  In general, users are not aware of such "forbidden" sequences.

4.5.3.2 Timeouts

  An SMTP client MUST provide a timeout mechanism.  It MUST use per-
  command timeouts rather than somehow trying to time the entire mail
  transaction.

D.1 A Typical SMTP Transaction Scenario

  S: 220 foo.com Simple Mail Transfer Service Ready
  C: EHLO bar.com
  S: 250-foo.com greets bar.com
  S: 250-8BITMIME
  S: 250-SIZE
  S: 250-DSN
  S: 250 HELP
  C: MAIL FROM:<Smith@bar.com>
  S: 250 OK
  C: RCPT TO:<Jones@foo.com>
  S: 250 OK
  C: RCPT TO:<Green@foo.com>
  S: 550 No such user here
  C: RCPT TO:<Brown@foo.com>
  S: 250 OK
  C: DATA
  S: 354 Start mail input; end with <CRLF>.<CRLF>
  C: Blah blah blah...
  C: ...etc. etc. etc.
  C: .
  S: 250 OK
  C: QUIT
  S: 221 foo.com Service closing transmission channel
