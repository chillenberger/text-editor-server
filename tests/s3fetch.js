import fs from "fs";

const data = {
  'url': 'https://codoc-mz8buped.s3.us-west-2.amazonaws.com/',
  'fields': {
    'key': 'object_name.txt',
    'x-amz-algorithm': 'AWS4-HMAC-SHA256',
    'x-amz-credential': 'AKIAWODIS6LHTTDBQV7U/20260218/us-west-2/s3/aws4_request',
    'x-amz-date': '20260218T234448Z',
    'policy': 'eyJleHBpcmF0aW9uIjogIjIwMjYtMDItMTlUMDA6NDQ6NDhaIiwgImNvbmRpdGlvbnMiOiBbeyJidWNrZXQiOiAiY29kb2MtbXo4YnVwZWQifSwgeyJrZXkiOiAib2JqZWN0X25hbWUudHh0In0sIHsieC1hbXotYWxnb3JpdGhtIjogIkFXUzQtSE1BQy1TSEEyNTYifSwgeyJ4LWFtei1jcmVkZW50aWFsIjogIkFLSUFXT0RJUzZMSFRUREJRVjdVLzIwMjYwMjE4L3VzLXdlc3QtMi9zMy9hd3M0X3JlcXVlc3QifSwgeyJ4LWFtei1kYXRlIjogIjIwMjYwMjE4VDIzNDQ0OFoifV19',
    'x-amz-signature': '04e2c23cff7535702297ca03ec1f8ffa281a03e5a4226a1f9017acba3f33c54a'
  }
}

const formData = new FormData();

for (const [key, value] of Object.entries(data.fields)) {
  formData.append(key, value);
}

const fileBuffer = fs.readFileSync("./tests/test.txt");
const file = new File([fileBuffer], "test.txt", { type: "text/plain" });
formData.append("file", file);

fetch(data.url, {
  method: "POST",
  body: formData,
}).then((response) => {
  console.log(response);
}).catch((error) => {
  console.log(error);
})