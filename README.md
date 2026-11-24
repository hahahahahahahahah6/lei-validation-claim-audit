# Legal entity identifier claim audit

This offline static audit compares documentation about identifier judgments with Python call patterns. It reads the root README and Markdown files under a docs directory, ignores fenced code, and treats inline code as prose. It never executes inspected code or contacts a network.

Install a distribution with pip, then run:

```sh
lei-validation-claim-audit audit [repo] [--fail-on high|medium] [--ignore PREFIX] [--json] [--verbose]
python3 -m lei_validation_claim_audit audit [repo]
lei-validation-claim-audit --version
```

The repository defaults to the current directory. Repeat the single-value ignore option for multiple relative path prefixes. The default failure threshold is high; medium also fails for test-only evidence. Exit status 0 means no finding reaches the threshold, 2 means a finding reaches it, and 1 means a usage or I/O error. JSON output contains a findings array.

The possible finding identifiers are:

```
documented-lei-validation-claim-false
documented-no-lei-validation-claim-false
```

An affirmative claim without production evidence is high severity, or medium when the only evidence is in tests. A denial contradicted by production evidence is high severity. With no Python files, an affirmative claim is high severity and a denial passes.

Supported calls include the following library routes and the generic named calls listed in the source. Imports and aliases are resolved within one module; local definitions and rebinding can shadow imports. Files in fixtures, docs, examples and tests are excluded from production evidence, while test files count separately. Symlinks and syntax-invalid files provide no evidence.

```
from stdnum import lei
lei.validate(value)
lei.is_valid(value)
```

## Differentiation

This audit does not cover the following neighbouring capabilities.

Whether input is checked at all belongs to generic validation.

ISBN-10 and ISBN-13 check digits concern book numbers.

ISSN check digits concern serial publications.

IBAN check digits concern bank account numbers.

A universally unique identifier has a different format.

Semantic version strings have their own format.

Hardware addresses have their own format.

Bank identifier codes have their own format.

Cron expression checking judges schedule syntax.

Cron expression description converts a schedule to prose.

Scheduled execution runs a job on a schedule.

Calendar date checking concerns real dates.

Timeouts limit how long a call may run.

Payment processing takes a card payment.

Card extraction reads card details from a document.

Authentication can prove account possession through a one-time code or confirmation link.

Password verification compares a password with a stored hash.

Password hashing prepares a password for storage.

Password generation creates random passwords.

PDF encryption protects a document with a password.

Email delivery sends mail.

SMS delivery sends a text to a number.

Document extraction reads data from documents.

Barcode scanning decodes a code from an image.

Email address checking concerns format or deliverability.

Phone number checking concerns format or regional validity.

Password strength checking judges password strength.

JSON Schema checking compares data with a schema.

Card number checking concerns a recognised brand and the Luhn algorithm.

Domain checking concerns host names.

URL checking concerns web addresses.

IP address checking concerns numeric addresses.

JSON decoding parses text into a value.

Regular expression matching finds patterns.

URL parsing splits a web address into parts.

Fetching a web address retrieves a remote resource.

DNS resolution looks up a name.

Barcode generation encodes an account number into a strip.

Account number extraction reads a number from a document.

Vehicle number extraction reads a number from a registration document or image.

Vehicle number decoding splits its sections or finds make, model and year.

Vehicle history lookup retrieves a vehicle's past.

Hexadecimal color checking concerns color strings.

ORCID checking concerns researcher identifiers.

ISNI checking concerns 16-digit name identifiers.

DOI validation concerns whether a digital object identifier names a work, and DOI resolution concerns whether that identifier resolves.

CUSIP checking concerns nine-character national securities identifiers.

SEDOL checking concerns seven-character London identifiers.

ISIN checking concerns twelve-character securities identifiers with a different check digit.

Market data lookup fetches a security record.

Securities identifier extraction reads a number from a document.

IMEI checking concerns fifteen-digit mobile device identifiers.

MEID checking concerns fourteen-digit hexadecimal mobile device identifiers.

General serial number checking covers a wider class of identifiers.

GLEIF registry lookup fetches an entity record.

Identifier conversion translates between securities and legal entity identifiers.

Registration through a Local Operating Unit issues a new identifier.

Identifier extraction reads a legal entity identifier from a document or photo.

The audit does not cover spreadsheet reading claims.

The audit does not cover spreadsheet generation claims.

The audit does not cover word-document reading claims.

The audit does not cover word-document generation claims.

The audit does not cover presentation reading claims.

The audit does not cover presentation generation claims.

The audit does not cover PDF extraction claims.

The audit does not cover PDF generation claims.

The audit does not cover PDF merging claims.

The audit does not cover PDF splitting claims.

The audit does not cover PDF rotation claims.

The audit does not cover PDF form-filling claims.

The audit does not cover PDF watermarking claims.

The audit does not cover PDF redaction claims.

The audit does not cover PDF compression claims.

The audit does not cover PDF annotation claims.

The audit does not cover table extraction claims.

The audit does not cover OCR claims.

The audit does not cover document extraction claims.

The audit does not cover e-signature claims.

The audit does not cover screen recording claims.

The audit does not cover video generation claims.

The audit does not cover QR code generation claims.

The audit does not cover barcode generation claims.

The audit does not cover barcode scanning claims.

The audit does not cover audio mixing claims.

The audit does not cover audio generation claims.

The audit does not cover audio editing claims.

The audit does not cover source separation claims.

The audit does not cover speech recognition claims.

The audit does not cover text-to-speech claims.

The audit does not cover noise suppression claims.

The audit does not cover music generation claims.

The audit does not cover music transcription claims.

## Limitations

```
validate lei
```

The bare phrase above can refer to a manual runbook step rather than an implemented capability, so a human must review the finding.

```
lei validation
```

The bare phrase above can refer to a roadmap feature rather than an implemented capability, so a human must review the finding.

The bare phrase above can also refer to a sentence produced by an external service showing a validity result at upload time, rather than an implemented capability, so a human must review the finding.

```
lei validator
```

The bare phrase above can refer to a hosted web page rather than an implemented capability, so a human must review the finding.

```
lei check
```

The bare phrase above can refer to a field-presence lint rule rather than an implemented capability, so a human must review the finding.

```
check lei
```

The bare phrase above can refer to a manual runbook step rather than an implemented capability, so a human must review the finding.

```
verify lei
```

The bare phrase above can refer to a visual confirmation of the counterparty rather than an implemented capability, so a human must review the finding.

```
lei code validation
```

The bare phrase above can refer to a field-presence check rather than an implemented capability, so a human must review the finding.

```
valid lei
```

The bare phrase above can refer to an example value rather than an implemented capability, so a human must review the finding.

```
lei is valid
```

The bare phrase above can refer to example output rather than an implemented capability, so a human must review the finding.

```
lei is invalid
```

The bare phrase above can refer to example error text rather than an implemented capability, so a human must review the finding.

```
lei validity
```

The bare phrase above can refer to a configuration flag or column name rather than an implemented capability, so a human must review the finding.

```
lei format validation
```

The bare phrase above can refer to a format description rather than an implemented capability, so a human must review the finding.

```
validate lei number
```

The bare phrase above can refer to a shape-only judgment without the LOU leg rather than an implemented capability, so a human must review the finding.

```
lei number validation
```

The bare phrase above can refer to a specification section rather than an implemented capability, so a human must review the finding.

```
validate lei code
```

The bare phrase above can refer to a manual runbook step rather than an implemented capability, so a human must review the finding.

```
check lei code
```

The bare phrase above can refer to a manual runbook step rather than an implemented capability, so a human must review the finding.

```
validate lei identifier
```

The bare phrase above can refer to a manual runbook step rather than an implemented capability, so a human must review the finding.

```
lei identifier validation
```

The bare phrase above can refer to a specification section rather than an implemented capability, so a human must review the finding.

```
lei entity validation
```

The bare phrase above can refer to a specification section rather than an implemented capability, so a human must review the finding.

```
lei number check
```

The bare phrase above can refer to an onboarding checklist item rather than an implemented capability, so a human must review the finding.

The bare word LEI alone is not a claim because it can name an identifier, a garland or a person.

The words LEI number alone do not assert a judgment.

The words validate identifier alone can describe any identifier.

The words check digit alone do not assert a judgment.

The words MOD 97 alone also describe the algorithm used for IBANs.

The word LOU alone names an issuing organisation.

The words legal entity alone do not assert a judgment about its identifier.

The word GLEIF alone names a registry.

A compact call strips separators and changes case without judging the value.

A bare MOD 97-10 validation call also applies to IBANs and has no identifier-specific leg.

The library accepts off-length inputs with a passing checksum, including 213800KUD8LAJWSQ96 and 213800KUD8LAJWSQ9D141.

The library accepts non-00 reserved characters with a passing checksum, such as 2138XXKUD8LAJWSQ9D52.

A registry lookup retrieves a record rather than judging the string.

Conversion between securities and entity identifiers does not judge either string.

Registration or issuance creates an identifier rather than judging a supplied string.

A length check alone does not check digits.

A Local Operating Unit membership check alone does not check digits.

A checksum call without an identifier-specific leg is not evidence.

A regular expression match alone is not evidence.

A validate call on an unrecognised base is missed even when the object came from a helper or another module.

A bare library import without a call is not evidence.

A roadmap, changelog or TODO in scanned prose still counts as a claim.

A denial outside the recognised list may leave an affirmative match.

A top-level changelog outside the selected documentation is invisible.

Evidence split across modules does not count.

A locally defined route name shadows the corresponding call.

Dead code counts because the audit does not execute code.

A subprocess invoking an external checker is not evidence.

A generic input check is not evidence for this identifier.

An email check is not evidence for this identifier.

A phone number check is not evidence for this identifier.

A URL check is not evidence for this identifier.

An IP address check is not evidence for this identifier.

A domain check is not evidence for this identifier.

An ISBN check is not evidence for this identifier.

An ISSN check is not evidence for this identifier.

An IBAN check is not evidence for this identifier.

An ISIN check is not evidence for this identifier.

An IMEI check is not evidence for this identifier.

Static patterns do not establish semantic correctness.

Alias chains beyond the tracer are missed.

Only exact phrases are recognised, not their full meaning.

Each route must appear within one module.

