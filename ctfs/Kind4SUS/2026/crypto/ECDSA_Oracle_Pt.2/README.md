mightygibbon

Following our initial deployment, we updated the ECDSA oracle to handle higher throughput and save expensive CPU cycles. The internal logic has been entirely rewritten to prioritize raw signing speed while maintaining strict security. This new version is much better, so feel free to stress-test it with up to 34 signatures.
