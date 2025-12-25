using Microsoft.EntityFrameworkCore;
using PetZone.Models;

var builder = WebApplication.CreateBuilder(args);

// Force listen on all network interfaces
builder.WebHost.UseUrls("http://0.0.0.0:5019");

var connectionString = "Host=localhost;Database=PetZoneDB;Username=postgres;Password=123456"; // Thay pass của bạn
builder.Services.AddDbContext<PetZoneDbContext>(options =>
    options.UseNpgsql(connectionString));
// Add services to the container.
builder.Services.AddCors(options => {
    options.AddDefaultPolicy(policy => {
        policy.WithOrigins("http://localhost:5173")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

//app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();
app.UseCors();
app.Run();
