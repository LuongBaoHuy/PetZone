using System;
using System.Collections.Generic;

namespace PetZone.Models;

public partial class AiDetection
{
    public int Id { get; set; }

    public bool HasPet { get; set; }

    public decimal? ConfidenceScore { get; set; }

    public string? Note { get; set; }

    public DateTime? CreatedAt { get; set; }
}
