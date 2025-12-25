using System;
using System.Collections.Generic;

namespace PetZone.Models;

public partial class SensorReading
{
    public int Id { get; set; }

    public decimal? Temperature { get; set; }

    public decimal? Humidity { get; set; }

    public int? PresenceEnergy { get; set; }

    public int? MovementEnergy { get; set; }

    public int? Distance { get; set; }

    public DateTime? CreatedAt { get; set; }
}
