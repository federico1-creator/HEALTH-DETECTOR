float acquisisco_temp()
// void
{
  t= mlx.readObjectTempC();
  float ambiente= mlx.readAmbientTempC();

  return t;
  
}
