using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

namespace PetZone.Models;

public partial class PetZoneDbContext : DbContext
{
    public PetZoneDbContext()
    {
    }

    public PetZoneDbContext(DbContextOptions<PetZoneDbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<AiDetection> AiDetections { get; set; }

    public virtual DbSet<DeviceActivity> DeviceActivities { get; set; }

    public virtual DbSet<FeedingLog> FeedingLogs { get; set; }

    public virtual DbSet<SensorReading> SensorReadings { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
#warning To protect potentially sensitive information in your connection string, you should move it out of source code. You can avoid scaffolding the connection string by using the Name= syntax to read it from configuration - see https://go.microsoft.com/fwlink/?linkid=2131148. For more guidance on storing connection strings, see https://go.microsoft.com/fwlink/?LinkId=723263.
        => optionsBuilder.UseNpgsql("Host=localhost;Database=PetZoneDB;Username=postgres;Password=123456");

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<AiDetection>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("ai_detections_pkey");

            entity.ToTable("ai_detections");

            entity.Property(e => e.Id).HasColumnName("id");
            entity.Property(e => e.ConfidenceScore)
                .HasPrecision(5, 2)
                .HasColumnName("confidence_score");
            entity.Property(e => e.CreatedAt)
                .HasDefaultValueSql("CURRENT_TIMESTAMP")
                .HasColumnName("created_at");
            entity.Property(e => e.HasPet).HasColumnName("has_pet");
            entity.Property(e => e.Note)
                .HasMaxLength(255)
                .HasColumnName("note");
        });

        modelBuilder.Entity<DeviceActivity>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("device_activities_pkey");

            entity.ToTable("device_activities");

            entity.Property(e => e.Id).HasColumnName("id");
            entity.Property(e => e.ActionType)
                .HasMaxLength(20)
                .HasColumnName("action_type");
            entity.Property(e => e.CreatedAt)
                .HasDefaultValueSql("CURRENT_TIMESTAMP")
                .HasColumnName("created_at");
            entity.Property(e => e.DeviceName)
                .HasMaxLength(50)
                .HasColumnName("device_name");
            entity.Property(e => e.TriggerReason)
                .HasMaxLength(255)
                .HasColumnName("trigger_reason");
        });

        modelBuilder.Entity<FeedingLog>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("feeding_logs_pkey");

            entity.ToTable("feeding_logs");

            entity.Property(e => e.Id).HasColumnName("id");
            entity.Property(e => e.AmountGram)
                .HasDefaultValue(50)
                .HasColumnName("amount_gram");
            entity.Property(e => e.CreatedAt)
                .HasDefaultValueSql("CURRENT_TIMESTAMP")
                .HasColumnName("created_at");
            entity.Property(e => e.IsSuccessful)
                .HasDefaultValue(true)
                .HasColumnName("is_successful");
            entity.Property(e => e.TriggerSource)
                .HasMaxLength(50)
                .HasColumnName("trigger_source");
        });

        modelBuilder.Entity<SensorReading>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("sensor_readings_pkey");

            entity.ToTable("sensor_readings");

            entity.HasIndex(e => e.CreatedAt, "idx_sensor_time");

            entity.Property(e => e.Id).HasColumnName("id");
            entity.Property(e => e.CreatedAt)
                .HasDefaultValueSql("CURRENT_TIMESTAMP")
                .HasColumnName("created_at");
            entity.Property(e => e.Distance).HasColumnName("distance");
            entity.Property(e => e.Humidity)
                .HasPrecision(5, 2)
                .HasColumnName("humidity");
            entity.Property(e => e.MovementEnergy).HasColumnName("movement_energy");
            entity.Property(e => e.PresenceEnergy).HasColumnName("presence_energy");
            entity.Property(e => e.Temperature)
                .HasPrecision(5, 2)
                .HasColumnName("temperature");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
