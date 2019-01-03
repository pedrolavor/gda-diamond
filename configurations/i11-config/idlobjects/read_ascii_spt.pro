;=====================================================================================
;THE FOLLOWING PROCEDURES AND FUNCTIONS:
;   pro ra_parse_column_values
;   function ra_split_csv
;   pro ra_parse_delim_values
;   function ra_get_next_record
;   function ra_read_from_templ
;   function ra_valid_template
;   function ra_stringit
;   function ra_guess_columns
;   function ra_check_file
;   function read_ascii_create_struct
;   function read_ascii_spt
;
;ARE ALL TAKEN FROM THE IDL LIBRARY PRO READ_ASCII. THE ONLY DIFFERENCES ARE
;   (1) THE NAME OF READ_ASCII_SPT
;   (2) ra_check_file HAS BEEN ALTERED TO STOP IT CHECKING THE FILE'S read AND ASCII
;       ATTTRIBUTES, WHICH UNDER GOOD OLD LINUX CAUSES A PROBLEM WITH FILES WRITTEN
;       BY A DIFFERENT USER ID POSSIBLY TO THE ONE RUNNING THE REBIN
;   (3) read_ascii_spt HAS BEEN ALTERED TO FORCE THE tth VALUES TO BE READ AS DOUBLES
;=====================================================================================
;A LINE OF $'s MARK THE END OF THE STOLEN CODE AND MY BEAUTIFULLY WITTEN REBIN PROGRAM
;=====================================================================================
;
;--------------------------------------------------------------------------------
pro ra_parse_column_values, line, types, p_vals, rec_count, $
    locs, lengths, missingValue, num_fields

    compile_opt HIDDEN, STRICTARR

    on_ioerror, column_cast_failed

    nf1 = num_fields - 1
    for i=0, nf1 do begin

        if (types[i] ne 0) then begin ; (0 == skip field.)
            token = (i eq nf1) ? STRTRIM(STRMID(line, locs[i]),2) : $
                STRTRIM(STRMID(line, locs[i], lengths[i]),2)
            ; Assign substring to the variable. This will automatically do
            ; any necessary type conversions.
            (*p_vals[i])[rec_count] = (STRLEN(token) ne 0) ? token : $
                (types[i] eq 7) ? token : missingValue
            continue
column_cast_failed:
            message, /reset
            (*p_vals[i])[rec_count] = missingValue
        endif
    endfor  ; i
end
; -----------------------------------------------------------------------------
function ra_split_csv, lineIn

  compile_opt idl2, hidden

  ; First replace escaped quote characters, which look like "",
  ; with a harmless upper-byte character.
  line = STRJOIN(STRTOK(lineIn, '""', /REGEX, /EXTRACT), STRING(254b))

  quoteLoc = STRTOK(line, '"', /PRESERVE_NULL)
  n = N_ELEMENTS(quoteLoc)

  ; Since we preserved nulls above, there should always be an odd
  ; number of quote-separated tokens... If the quotes are paired correctly.
  if (n gt 2 && (n mod 2) eq 1) then begin

    commaLoc = STRTOK(line, ',', /PRESERVE_NULL, LENGTH=length)
    line = STRMID(line, commaLoc, length)

    ; Add a backslash escape in front of all commas that lie within quotes.
    for i=1,n-1,2 do begin
      indx = WHERE(commaLoc gt quoteLoc[i] and commaLoc lt quoteLoc[i+1], nInside)
      if (nInside gt 0) then line[indx-1] += '\'
    endfor

    line = STRJOIN(line, ',')

  endif

  ; Remove quotes that are just surrounding fields.
  line = STRJOIN(STRTOK(line, '"', /EXTRACT))

  ; Put back the quotes that were in the actual field.
  line = STRJOIN(STRTOK(line, STRING(254b), /EXTRACT), '"')

  return, STRTOK(line, ',', ESCAPE='\', /EXTRACT, /PRESERVE_NULL)
end
; -----------------------------------------------------------------------------
pro ra_parse_delim_values, line, types, p_vals, rec_count, $
  delimit, missing_value, whitespace_delimited, CSV=csvIn

  compile_opt HIDDEN, STRICTARR

  csv = Keyword_Set(csvIn)

  if (csv) then begin
    toks = ra_split_csv(line)
  endif else begin
    ; Remove whitespace from beginning and end.
    toks = whitespace_delimited ? STRTOK(line, /EXTRACT) : $
      STRTRIM(STRTOK(line, delimit, /EXTRACT, /PRESERVE_NULL), 2)
  endelse

  length = STRLEN(toks)

  on_ioerror, delim_cast_failed

  n_types = N_ELEMENTS(types)
  n_toks = N_ELEMENTS(toks)
  nMin1 = (n_types < n_toks) - 1

  ; Loop up to the end of the tokens or the number of fields, whichever
  ; is smaller. Empty fields will be filled in after this loop.
  for i=0,nMin1 do begin

    if (types[i] ne 0) then begin ; (0 == skip field.)
        ; Assign the substring to the variable. This will automatically do
        ; any necessary type conversions.
        (*p_vals[i])[rec_count] = (length[i] ne 0) ? toks[i] : $
            ((types[i] eq 7) ? toks[i] : missing_value)
        ; If successful conversion, then continue the loop.
        continue
delim_cast_failed:
        ; If failed conversion, suppress the error and fill with missing.
        message, /reset
        (*p_vals[i])[rec_count] = missing_value
    endif
  endfor


  ; Need to fill in extra fields with missing.
  if (n_toks lt n_types) then begin
    for i=n_toks, n_types-1 do begin
        if (types[i] gt 0) then $
            (*p_vals[i])[rec_count] = missing_value
    endfor
  endif

end         ; ra_parse_delim_values
; -----------------------------------------------------------------------------
function ra_get_next_record, template, unit, lines
  ;
  COMPILE_OPT hidden, strictarr

  on_ioerror, end_of_file
  line = ''
  count = 0

  ;  Checking for comments...
  ;
  if (template.commentSymbol ne '') then begin
    while (count lt n_elements(lines)) do begin
      readf, unit, line
      pos = strpos(line, template.commentSymbol, 0)
      if (strtrim(line,2) ne '' and pos[0] ne 0) then begin
        lines[count] = (pos[0] eq -1) ? line : strmid(line,0,pos[0])
        count = count + 1
      endif
    endwhile

  ;  NOT checking for comments...
  ;
  endif else begin
    while (count lt n_elements(lines)) do begin
      readf, unit, line
      if (strlen(strtrim(line,2)) ne 0) then begin
        lines[count] = line
        count = count + 1
      endif
    endwhile
  endelse

  return, 0 ; success

end_of_file:
  ; If read failed, suppress message and return EOF.
  message, /reset
  return, 1  ; failure, EOF

end   ; ra_get_next_record
; -----------------------------------------------------------------------------
function ra_read_from_templ, $
    name, $     ; IN: name of ASCII file to read
    template, $     ; IN: ASCII file template
    start_record, $ ; IN: first record to read
    records_to_read, $  ; IN: number of records to read
    doVerbose, $    ; IN: 1B = print runtime messages
    num_fields_read, $  ; OUT: number of fields successfully read
    fieldNames, $       ; OUT: associated name of each field read
    rec_count, $    ; OUT: number of records successfully read
    num_blocks, $    ; OUT: number of blocks of data
    header=header, $   ; OUT: (opt) header read
    CSV=csvIn

  COMPILE_OPT hidden, strictarr

  ;  Set default numbers.
  ;
  num_fields_read = 0
  num_blocks = 0L

  ;  Catch errors.
  catch, error_status
  if (error_status ne 0) then begin
    CATCH, /CANCEL
    MESSAGE, /INFO, 'Unexpected Error: ' + !ERROR_STATE.msg
    MESSAGE, /RESET
    rec_count = 0l
    return, 0
  endif

  ;  Open the file.
  ;
  openr, unit, name, /get_lun

  ;  Set various parameters.
  ;
  blk_size = 1000  ; each block holds this many records
  blk_count = 500  ; number of blocks we can have
  blk_grow  = 500
  current_block = 0L
  lines_per_record = n_elements(template.fieldCount)
  num_fields = template.fieldCount
  tot_num_fields = total(template.fieldCount)
  types = template.fieldTypes
  locs = template.fieldLocations
  ; The length of the last field depends upon the line length,
  ; so here just make it some arbitrary number.
  fieldLengths = (n_elements(locs) gt 1) ? [locs[1:*],0] - locs : 0

  ;  Define an array of variables for each field.
  ;
  p_vals = ptrarr(tot_num_fields, blk_count)
  for i=0, tot_num_fields-1 do $
    if (types[i] gt 0) then $
      p_vals[i, current_block] = ptr_new(make_array(blk_size, type=types[i]))

  ;  Read the header and skip to the start of the data.
  ;
  dataStart = template.dataStart
  if (dataStart gt 0) then begin
    if (doVerbose) then $
      print, 'Reading header of ' + strtrim(string(dataStart), 2) + $
        ' lines ...', format='(A/)'
    header = strarr(dataStart)
    readf, unit, header
  endif else $
    header = ''

  ;  Skip to the start of requested data.
  ;
  lines = strarr(lines_per_record)
  if ((doVerbose) and (start_record gt 0)) then $
    print, 'Skipping ' + strtrim(string(start_record), 2) + ' records ...', $
      format='(A/)'
  for i = 0L, start_record-1 do $
    end_reached = RA_GET_NEXT_RECORD(template, unit, lines)

    if template.delimiter eq 32b then begin
      delim_str = string([32b, 9b])
      whitespace_delimited = 1b
    end else begin
      delim_str = string(template.delimiter)
      whitespace_delimited = 0b
    endelse

    nRecord1 = (records_to_read gt 0) ? records_to_read-1L : 2147483647L
    for rec_count = 0L, nRecord1 do begin

        ;  Read a record.
        ;
        end_reached = RA_GET_NEXT_RECORD(template, unit, lines)
        if (end_reached) then break ; out of the for loop

        ;xxx
        if (doVerbose) then $
        print, 'Processing sequential record ' + $
          strtrim(string(rec_count+1), 2) + ' ...'

        anchor = 0
        rc = rec_count-current_block*blk_size

        ;  For each line in the record...
        ;
        for i=0,lines_per_record-1 do begin

            if (template.delimiter eq 0B) then begin
                ; nice columned data...
                ra_parse_column_values, lines[i], $
                    types[ anchor:anchor+num_fields[i]-1], $
                    p_vals[anchor:anchor+num_fields[i]-1, current_block], $
                    rc, $
                    locs[ anchor:anchor+num_fields[i]-1], $
                    fieldLengths[anchor:anchor+num_fields[i]-1], $
                    template.missingValue, $
                    num_fields[i]
            endif else begin
                ; data separated by a delimiter...
                ra_parse_delim_values, lines[i], $
                    types[ anchor:anchor+num_fields[i]-1], $
                    p_vals[anchor:anchor+num_fields[i]-1, current_block], $
                    rc, $
                    delim_str, $
                    template.missingValue, $
                    whitespace_delimited, CSV=csvIn
            endelse
            anchor = anchor + num_fields[i]
        endfor  ; i

        ; If block is now full,
        ; Allocate and point to a new block
        ;
        if ((rec_count+1) mod blk_size eq 0) then begin
            current_block = current_block + 1
            if (current_block eq blk_count) then begin
                p_vals = [[p_vals], [ptrarr(tot_num_fields, blk_grow)]]
                blk_count = blk_count + blk_grow
            endif
            for i=0, tot_num_fields-1 do if (types[i] gt 0) then $
                p_vals[i, current_block] = $
                    ptr_new(make_array(blk_size, type=types[i]))
        endif  ; new block
    endfor  ; read

  ; ------------------------------------
  free_lun, unit

  if (doVerbose) then $
    print, 'Total records read:  ' + strtrim(string(rec_count), 2), $
      format='(A/)'

    ; No records were read.
    if (rec_count eq 0) then begin
        PTR_FREE, p_vals
        return, 0
    endif

    ;  If records were read ...
    ;  Set the output arrays to exactly the correct size.
    ;
    for i=0, tot_num_fields-1 do begin
      if (p_vals[i,current_block] ne ptr_new()) then begin
        if (rec_count gt current_block*blk_size) then begin
          *p_vals[i,current_block] = $
            (*p_vals[i,current_block])[0:rec_count-current_block*blk_size-1]
        endif else begin ; block is allocated, but empty
            ptr_free, p_vals[i,current_block]
        endelse
      endif
    endfor
    if (rec_count gt current_block*blk_size) then begin
      num_blocks = current_block + 1
    endif else begin
      num_blocks = current_block
    endelse

    ;  Check the groups array and arrange the output pointers into
    ;  (potentially) groups of 2-D arrays.
    ;
    groups = template.fieldGroups

    ;  Don't include any groups which are skipped fields.
    ;
    ptr = where(types eq 0, numSkip)
    for i=0, numSkip-1 do groups[ptr[i]] = max(groups) + 1

    ;  Concatenate 1-D arrays into multi arrays based upon groupings.
    ;
    uptr = uniq(groups, sort(groups))
    if (n_elements(uptr) lt n_elements(groups)) then begin
      for i=0, n_elements(uptr)-1 do begin
          for b=0, num_blocks-1 do begin
            lptr = where(groups eq groups[uptr[i]], lcount)
            if (lcount gt 1) then begin
              p_new = p_vals[lptr[0],b]
              for j=1,lcount-1 do begin
                *p_new = [[temporary(*p_new)],[temporary(*p_vals[lptr[j],b])]]
                ptr_free, p_vals[lptr[j],b]
                p_vals[lptr[j],b] = ptr_new()
              endfor
              *p_new = transpose(temporary(*p_new))
            endif
          endfor
      endfor
    endif

    ;  Return the pointers that contain data, if any.
    ;  and the associated fieldNames for these pointers
    ;
    ptr = where(p_vals[*,0] ne ptr_new(), num_fields_read)

    if (num_fields_read gt 0) then begin ; data successfully read
      fieldNames = template.fieldNames[ptr]
      return, p_vals[ptr,*]
    endif else begin                           ; no data read
      rec_count = 0l
      return, 0
    endelse

end         ; ra_read_from_templ
; -----------------------------------------------------------------------------
function ra_valid_template, $
  template, $       ; IN: template to check
  message           ; OUT: error message if the template is not valid

  COMPILE_OPT hidden, strictarr

  message = ''

  ;  Make sure it's a structure.
  ;
  sz = size(template)
  if (sz[sz[0]+1] ne 8) then begin
    message = 'Template is not a structure.'
    RETURN, 0B
  endif

  ;  Get tag names and make sure version field is present.
  ;
  tagNamesFound = TAG_NAMES(template)
  void = WHERE(tagNamesFound eq 'VERSION', count)
  if (count ne 1) then begin
    message = 'Version field missing from template.'
    RETURN, 0B
  endif

  ;  Do checking based on version.
  ;
  case (template.version) of

    1.0: begin

      ;  Set the names of the required tags (version alread checked).
      ;
      tagNamesRequired = STRUPCASE([ $
        'dataStart', 'delimiter', 'missingValue', 'commentSymbol', $
        'fieldCount', 'fieldTypes', 'fieldNames', 'fieldLocations', $
        'fieldGroups'])

      ;  Check that all of the required tags are present.
      ;
      for seqTag = 0, N_ELEMENTS(tagNamesRequired)-1 do begin
        tag = tagNamesRequired[seqTag]
        void = WHERE(tagNamesFound eq tag, count)
        if (count ne 1) then begin
          message = tag + ' field missing from template.'
          RETURN, 0B
        endif
      endfor

    end

    else: begin
      message = 'The only recognized template version is 1.0 (float).'
      RETURN, 0B
    end
  endcase

  ; Check for valid structure tag names before we try to
  ; read the file.
  for i=0,N_ELEMENTS(template.fieldNames)-1 do begin
    if (IDL_VALIDNAME(template.fieldNames[i], /CONVERT_SPACES) eq '') then begin
        message = 'Illegal field name: ' + template.fieldNames[i]
        return, 0b  ; failure
    endif
  endfor


  ;  Return that the template is valid.
  ;
  RETURN, 1B

end         ; ra_valid_template
; -----------------------------------------------------------------------------
function ra_stringit, value

  COMPILE_OPT hidden, strictarr

  result = STRTRIM( STRCOMPRESS( STRING(value) ), 2 )

  num = N_ELEMENTS(result)

  if (num le 1) then RETURN, result

  ;  If two or more values, concatenate them.
  ;
  delim = ' '
  ret = result[0]
  for i = 1, num-1 do $
    ret = ret + delim + result[i]

  RETURN, ret

end         ; ra_stringit
; -----------------------------------------------------------------------------
function ra_guess_columns, fname, dataStart, commentSymbol, delimiter

  COMPILE_OPT hidden, strictarr

  on_error, 2 ; Return to caller on error.

  catch, err_stat
  if err_stat ne 0 then begin
    catch, /cancel
    if n_elements(lun) gt 0 then $
      if (lun ne 0) then free_lun, lun
    message, !error_state.msg
  endif

  get_lun, lun
  openr, lun, fname

  if dataStart gt 0 then begin
    header = strarr(dataStart)
    readf, lun, header
  end

  line = ''
  end_reached = RA_GET_NEXT_RECORD({commentSymbol: commentSymbol}, $
    lun, line)

  if end_reached then $
    message, 'No columns found.'

  if delimiter eq ' ' then $
    positions = strtok(line) $
  else $
    positions = strtok(line, delimiter, /preserve_null)

  close, lun
  free_lun, lun
  return, n_elements(positions)
end
; -----------------------------------------------------------------------------
function ra_check_file, fname

  COMPILE_OPT hidden, strictarr

  if (SIZE(fname, /TYPE) ne 7) then $
    return, -1 ; filename isn't a string

  info = FILE_INFO(fname)
  if (~info.exists) then $
    return, -2
;  if (~info.read) then $
;    return, -3

;  success = QUERY_ASCII(fname)
   success=1
  return, success ? 1 : -4

end
; ------------------------------------------------------------------------
function read_ascii_create_struct, fieldnames, xData

    compile_opt idl2, hidden

    nFields = N_ELEMENTS(fieldnames)

    case (nFields) of

        0: return, 0   ; this shouldn't happen

        ; Create a structure with a single field.
        1: return, CREATE_STRUCT(fieldnames[0], TEMPORARY(*xData[0]))

        ; Create a structure with two fields.
        2: return, CREATE_STRUCT( $
            fieldnames[0], TEMPORARY(*xData[0]), $
            fieldnames[1], TEMPORARY(*xData[1]))

        ; Create a structure with three fields.
        3: return, CREATE_STRUCT( $
            fieldnames[0], TEMPORARY(*xData[0]), $
            fieldnames[1], TEMPORARY(*xData[1]), $
            fieldnames[2], TEMPORARY(*xData[2]))

        else: begin

        ; Divide into 4 equal-sized sets of pointers, and concatanate
        ; the structures. Four is somewhat arbitrary, but on average,
        ; this will then require only 1/4 of the memory, as compared
        ; to simply concatanating the fields onto the end.
        d = nFields/4
        ; Recursive call.
        return, CREATE_STRUCT( $
            READ_ASCII_CREATE_STRUCT(fieldnames[0:d-1], xData[0:d-1]), $
            READ_ASCII_CREATE_STRUCT(fieldnames[d:2*d-1], xData[d:2*d-1]), $
            READ_ASCII_CREATE_STRUCT(fieldnames[2*d:3*d-1], xData[2*d:3*d-1]), $
            READ_ASCII_CREATE_STRUCT(fieldnames[3*d:*], xData[3*d:*]))
        end

    endcase

end
; -----------------------------------------------------------------------------
function read_ascii_spt, $
    file, $             ; IN:
    RECORD_START=recordStart, $     ; IN: (opt)
    NUM_RECORDS=numRecords, $       ; IN: (opt)
    TEMPLATE=template, $        ; IN: (opt)
    DATA_START=dataStart, $     ; IN: (opt)
    DELIMITER=delimiter, $      ; IN: (opt)
    MISSING_VALUE=missingValue, $   ; IN: (opt)
    COMMENT_SYMBOL=commentSymbol, $ ; IN: (opt)
;    FIELDS=fields, $           ; IN: (opt)    [not implemented]
    VERBOSE=verbose, $          ; IN: (opt)
    HEADER=header, $            ; OUT: (opt)
    COUNT=count, $             ; OUT: (opt)
    CSV=csvIn, $
    CANCEL=cancel, $
    WBOPEN=wbopen, $
    _EXTRA=_extra

    COMPILE_OPT strictarr
  ;xxx
  ;later add a VERSION kw ?

  ;  Set to return to caller on error.
  ;
  ON_ERROR, 2


  ;  Set some defaults.
  ;
  count = 0
  currentVersion = 1.0
;  doVerbose = KEYWORD_SET(verbose)
  doVerbose=0

  ;  If no file specified, use DIALOG_PICKFILE
  ;
  if (n_elements(file) eq 0) then begin
    file = DIALOG_PICKFILE(/MUST_EXIST)
    if (file eq '') then RETURN, 0
  endif

  ; check that the file is readable and appears to be ASCII
  ;
  ret = ra_check_file(file)
  case ret of
    -1: MESSAGE, 'File name must be a string.'
    -2: MESSAGE, 'File "' + file + '" not found.'
    -3: MESSAGE, 'Error Reading from file "' + file + '"'
    -4: MESSAGE, 'File "' + file + '" is not a valid ASCII file.'
    else:
  endcase

  if ((N_ELEMENTS(template) eq 0) && KEYWORD_SET(wbopen)) then begin
    template = ASCII_TEMPLATE(file, CANCEL=cancel, WBOPEN=wbopen, _EXTRA=_extra)
    if ((N_ELEMENTS(cancel) ne 0) && (cancel ne 0)) then begin
      ;; return gracefully
      return, 0
    endif
  endif

  ;  Set which records to read.
  ;
  if (N_ELEMENTS(recordStart) ne 0) then recordStartUse = recordStart $
                                    else recordStartUse = 0
  if (N_ELEMENTS(numRecords) ne 0)  then numRecordsUse = numRecords $
                                    else numRecordsUse = 0
  if (N_ELEMENTS(template) gt 0) then begin
    if (not ra_valid_template(template, message)) then $
      MESSAGE, message

    versionUse      = template.version
    dataStartUse    = template.dataStart
    delimiterUse    = STRING(template.delimiter)
    missingValueUse = template.missingValue
    commentSymbolUse    = template.commentSymbol
  endif else begin
    versionUse      = currentVersion
    dataStartUse    = 0L
    delimiterUse    = ' '
    missingValueUse = !values.f_nan
    commentSymbolUse    = ''
  endelse

  if n_elements(dataStart) ne 0 then $
    dataStartUse = dataStart
  if n_elements(delimiter) ne 0 then $
    delimiterUse = delimiter
  if n_elements(missingValue) ne 0 then $
    missingValueUse = missingValue
  if n_elements(commentSymbol) ne 0 then $
    commentSymbolUse = commentSymbol

  if n_elements(dataStartUse) gt 1 then $
    message, 'DATA_START must be a scalar.'
  if n_elements(byte(delimiterUse)) gt 1 then $ ; Might want to remove this
    message, 'DELIMITER must be one character.' ; restriction in the future.

  ;  (For back version compatibility, we do not throw an error
  ;  here if n_elements(missingValueUse) gt 1).
  ;

  ;  The READ_ASCII that shipped with IDL 5.2.1 returns 0 when
  ;  an array of comment symbols is specified.  Set the error_state
  ;  in this case, but, for back version compatibility, continue
  ;  and reproduce the "return 0" behavior here.
  ;
  if n_elements(commentSymbolUse) gt 1 then begin
    message, $
      'Multiple comment symbols are not currently supported.', $
      /noprint, $
      /continue
    return, 0
  endif

  if n_elements(template) gt 0 then begin
    fieldCountUse   = template.fieldCount
    fieldTypesUse   = template.fieldTypes
    fieldNamesUse   = template.fieldNames
    fieldLocationsUse   = template.fieldLocations
    fieldGroupsUse  = template.fieldGroups
  endif else begin
    fieldCountUse = n_elements(fieldTypes) $
      > n_elements(fieldNames) $
      > n_elements(fieldLocations) $
      > n_elements(fieldGroups)
    if fieldCountUse le 0 then $
      fieldCountUse = ra_guess_columns( $
        file, $
        dataStartUse, $
        commentSymbolUse, $
        delimiterUse $
        )

    fieldTypesUse   = REPLICATE(4L, fieldCountUse)
    digits_str = strtrim(string(strlen(strtrim(string(fieldCountUse),2))),2)
    fstr = '(i' + digits_str + '.' + digits_str + ')'
    fieldNamesUse   = 'field' + STRING(INDGEN(fieldCountUse)+1, format=fstr)
    fieldLocationsUse   = LONARR(fieldCountUse)
    fieldGroupsUse  = INTARR(fieldCountUse)
  endelse

  if n_elements(fieldTypes) ne 0 then $
    fieldTypesUse = fieldTypes
  if n_elements(fieldNames) ne 0 then $
    fieldNamesUse = fieldNames
  if n_elements(fieldLocations) ne 0 then $
    fieldLocationsUse = fieldLocations
  if n_elements(fieldGroups) ne 0 then $
    fieldGroupsUse = fieldGroups

  ;  Error check the field data.
  ;
  lengths = [ $
    N_ELEMENTS(fieldTypesUse), $
    N_ELEMENTS(fieldNamesUse), $
    N_ELEMENTS(fieldLocationsUse), $
    N_ELEMENTS(fieldGroupsUse) $
    ]
  if (TOTAL(ABS(lengths - SHIFT(lengths, 1))) ne 0) then $
    MESSAGE, 'Field data (types/names/locs/groups) not the same length.'

  ;  Set the template to use.
  ;
  templateUse = { $
    version: versionUse, $
    dataStart: dataStartUse, $
    delimiter: BYTE(delimiterUse), $
    missingValue: missingValueUse, $
    commentSymbol: commentSymbolUse, $
    fieldCount: fieldCountUse, $
    fieldTypes: fieldTypesUse, $
    fieldNames: fieldNamesUse, $
    fieldLocations: fieldLocationsUse, $
    fieldGroups: fieldGroupsUse $
    }

  ;  Print verbose information.
  ;
  if (doVerbose) then begin
    PRINT, 'Using the following file attributes ...', FORMAT='(/A)'
    PRINT, '        Data Start:  ' + STRTRIM(STRING(dataStartUse), 2)
    PRINT, '         Delimiter:  ' + $
                             STRTRIM(STRING(FIX(BYTE(delimiterUse))), 2) + 'B'
    PRINT, '     Missing Value:  ' + STRTRIM(STRING(missingValueUse), 2)
    PRINT, '    Comment Symbol:  ' + commentSymbolUse
    PRINT, '      Field Counts:  ' + ra_stringit(fieldCountUse)
    PRINT, '      Field Types :  ' + ra_stringit(fieldTypesUse)
    PRINT, '      Field Names :  ' + ra_stringit(fieldNamesUse)
    PRINT, '      Field Locs  :  ' + ra_stringit(fieldLocationsUse)
    PRINT, '      Field Groups:  ' + ra_stringit(fieldGroupsUse)
    PRINT, '  Template Version:  ' + STRTRIM(STRING(versionUse), 2)
    PRINT
  endif

  ;  Try to read the file.
  ;
  pData = ra_read_from_templ(file, templateUse, recordStartUse, $
    numRecordsUse, doVerbose, numFieldsRead, FieldNames, count, num_blocks, $
    header=header, CSV=csvIn)

  ;  Return zero if no records read.
  ;
  if (count eq 0) then $
    RETURN, 0

  ; Concatenate the blocks into fields.
  ;
  xData = ptrarr(numFieldsRead)

    ; If an error occurs, free up our temp pointers.
    CATCH, err
    if (err ne 0) then begin
        CATCH, /CANCEL
        PTR_FREE, xData, pData
        MESSAGE, /REISSUE_LAST
        return, 0
    endif

  for f=0L, numFieldsRead-1 do begin
    type = SIZE(*pData[f,0], /TYPE)
    if f eq 0L then type=5; <---------------------------added by SPT force tth to be double rather than float
    dims = SIZE(*pData[f,0], /DIMENSIONS)
    n_dims = SIZE(*pData[f,0], /N_DIMENSIONS)
    if (count eq 1) then begin
    ; if the file contains a single record, it is really
    ; two-dimensional: n fields x 1 record
      n_dims = 2
      dims = lonarr(2)
      dims[0] = SIZE(*pData[f,0],/N_ELEMENTS)
    endif
    dims[n_dims-1] = count
    xData[f] = ptr_new(make_array(DIMENSION=dims, TYPE=type))
    start=0L

    for b=0L, num_blocks-1 do begin
      sz = SIZE(*pData[f,b],/N_ELEMENTS)
      stop = start + sz - 1
      (*xData[f])[start:stop] = *pData[f,b]
      ptr_free, pData[f,b]
      start = stop + 1
    endfor
  endfor

  ;  Put the fields into a structure.
  data = READ_ASCII_CREATE_STRUCT(fieldnames, xData)

  ;  Clean up the heap data.
  ;
  for f = 0L, numFieldsRead-1 do $
    PTR_FREE, xData[f]

  ;  Print verbose information.
  ;
  if (doVerbose) then begin
    PRINT, 'Output data ...'
    HELP, data, /STRUCTURES
    PRINT
  endif

  ;  Return the structure.
  ;
  RETURN, data

end         ; read_ascii
;$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


