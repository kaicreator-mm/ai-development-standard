#!/usr/bin/env node
// Independent ECMAScript syntax and semantics checks for all JSON Schema regex patterns.
// A Python jsonschema PASS does not establish ECMA-262 RegExp interoperability.
"use strict";
const fs = require("node:fs");
const schema = JSON.parse(fs.readFileSync("schemas/github/v4.14/structured-interaction.schema.json","utf8"));
let visited=0;
function walk(v, path) {
  if(Array.isArray(v)){v.forEach((x,i)=>walk(x,path+"/"+i));return;}
  if(!v || typeof v!=="object")return;
  for(const [key,value] of Object.entries(v)){
    if(key==="pattern"){
      if(typeof value!=="string")throw Error(path+": pattern not string");
      try {new RegExp(value,"u");}
      catch(e){throw Error(path+": non-portable ECMA-262 regex: "+e.message);}
      visited++;
    } else walk(value,path+"/"+key);
  }
}
walk(schema,"#");
const expression = new RegExp(schema.$defs.report.properties.manifest_ref.pattern,"u");
for(const good of [
  "object:private/reports/42/manifest.json",
  "https://github.com/org/repo/blob/0123456789abcdef0123456789abcdef01234567/manifest.json",
  "oss:private-bucket/42/r1/manifest.json"
]) {
  if(!expression.test(good))throw Error("valid stable ref rejected: "+good);
}
for(const invalid of [
  "https://s3.example/test?X-Amz-Signature=secret",
  "https://s3.example/test?x-amz-signature=secret",
  "https://oss.example/test?x-oss-signature=secret",
  "https://store/test?token=abc",
  "https://store/test#rev",
  "object:has space"
]){
  if(expression.test(invalid))throw Error("invalid/signed locator admitted: "+invalid);
}
if(visited<4)throw Error("unexpected loss of nested schema patterns: "+visited);
process.stdout.write("ECMA-262 RegExp interoperability PASS: "+visited+" pattern expressions checked\n");
