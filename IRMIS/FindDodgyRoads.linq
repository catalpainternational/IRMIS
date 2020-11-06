<Query Kind="Expression">
  <Connection>
    <ID>20bfd2c7-ded4-4272-aff6-9a169139c344</ID>
    <NamingServiceVersion>2</NamingServiceVersion>
    <Persist>true</Persist>
    <Driver Assembly="(internal)" PublicKeyToken="no-strong-name">LINQPad.Drivers.EFCore.DynamicDriver</Driver>
    <Server>127.0.0.1</Server>
    <Database>estrada_db</Database>
    <UserName>postgres</UserName>
    <SqlSecurity>true</SqlSecurity>
    <Password>AQAAANCMnd8BFdERjHoAwE/Cl+sBAAAAHpkHJZO2F0eEiaslY9fgqAAAAAACAAAAAAAQZgAAAAEAACAAAAAHa3rhrhkglxSnD82aDIqbVoQmrSoPL5rCzhQPdftqWwAAAAAOgAAAAAIAACAAAADuWoVLT9ShA/SwxKqBYz/p/1uNKIS0N05Zn+69J9ThNhAAAABO9hOLbjcSCT7I68a1KL6YQAAAAMEOcIQibgg3BWjb7eR6wIwB3qeFvbF1PNFKML/JD1XUA+i6xkxJ4yPvfXClKOwDfzN13uOeJ013awpucFmTjP8=</Password>
    <DisplayName>estrada_db</DisplayName>
    <DriverData>
      <Port>5432</Port>
      <EFProvider>Npgsql.EntityFrameworkCore.PostgreSQL</EFProvider>
      <UseNativeScaffolder>True</UseNativeScaffolder>
      <EFVersion>2.2.4</EFVersion>
    </DriverData>
  </Connection>
</Query>

AssetsRoads
.Where(ar => ar.GeojsonFile == null && ar.GeomStartChainage != null)
.OrderBy(ar => ar.RoadCode)
.ThenBy(ar => ar.GeomStartChainage)
.ThenBy(ar => ar.Id)
