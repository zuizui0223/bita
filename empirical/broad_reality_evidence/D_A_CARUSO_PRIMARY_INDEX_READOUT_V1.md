# Caruso 2019 primary-study index readout v1

## Scope

This is a bounded access and schema investigation of Caruso et al. 2019 (DOI
`10.1111/evo.13639`) as a possible **index to primary studies**. Caruso's floral
selection gradients remain outside the `d_A` effect registry throughout.

## Route recovered

```text
Caruso DOI -> DataCite explicitly related dataset -> Dryad DOI 10.5061/dryad.2v8c5g0
Dryad dataset metadata -> current version -> public file manifest
```

The file manifest lists two experimental-study database files:

```text
Exp_stud_dup_Dryad.xlsx      231,078 bytes
Exp_stud_NOTdup_Dryad.xls    451,584 bytes
```

This establishes that the Caruso project has an associated experimental-study data
resource. It does not establish that its rows are eligible `d_A` estimates.

## XLSX schema gate

For the XLSX candidate, the procedure was intentionally restricted to:

```text
1. resolve the public file metadata record;
2. obtain its canonical download route;
3. download at most 1 MiB;
4. retain only workbook sheet names, dimensions, and first-row field names.
```

The file metadata request returned HTTP 200, but the canonical public file-download
route returned **HTTP 401** before any workbook bytes were read.

```text
file metadata:             recovered
manifest:                  recovered
XLSX schema:               not recovered
reason:                    public file download unauthorized (HTTP 401)
primary-study IDs read:    0
primary-study effects read: 0
new B2 effects:            0
```

## Decision

```text
retain Caruso as a system seed only
stop this public dataset route before row-level extraction
```

The obstacle is an access limitation in the currently registered no-auth public API
route, not evidence that the underlying primary studies lack bibliographic or
trait-antagonism information. A future attempt would require a lawful authenticated
or author-provided data route; it must still extract each primary study separately
and pass the ordinary `d_A` C3/C4 gate.

## Boundary

This readout never uses Caruso's selection gradients as `d_A` effects and never
turns a dataset manifest, filename, or inaccessible file into a primary-study
estimate.