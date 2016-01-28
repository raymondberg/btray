
echo "Please enter your unique id and hit enter:"
read UNIQUE_ID

for i in `seq 1 10`; do
  curl -X POST --data 'bt_signature=fake-valid-signature-for-testing&bt_payload=VGhpcyBpcyBhIHRlc3QNClRoaXMgaXMgb25seSBhIHRlc3QNCklmIHlvdSB0cnkgYW55dGhpbmcgZnVubnkgaXQgd2lsbCBlbmQgcG9vcmx5Lg==' http://localhost:5000/endpoints/$UNIQUE_ID/
done
