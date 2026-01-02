"""
Script to remove all demo users and data while keeping only the admin account
"""

from app import app
from models.database import (
    db, User, UserRole, FarmerProfile, VendorProfile, LaborProfile,
    CropListing, VendorProduct, Order, OrderStatus, Payment, CostRecord,
    LaborHiring, Equipment, EquipmentRental, RecommendationHistory
)

def clear_demo_data():
    """Remove all demo data and users except admin"""
    with app.app_context():
        print("=" * 60)
        print("Clearing all demo users and data (keeping admin only)")
        print("=" * 60)
        
        # Get admin user(s) to preserve
        admin_users = User.query.filter_by(role=UserRole.ADMIN).all()
        admin_ids = [admin.id for admin in admin_users]
        
        print(f"\n✓ Found {len(admin_users)} admin user(s) to preserve:")
        for admin in admin_users:
            print(f"  - {admin.email}")
        
        # Count existing data
        print(f"\nCurrent database status:")
        print(f"  Users: {User.query.count()}")
        print(f"  Farmer Profiles: {FarmerProfile.query.count()}")
        print(f"  Vendor Profiles: {VendorProfile.query.count()}")
        print(f"  Labor Profiles: {LaborProfile.query.count()}")
        print(f"  Crop Listings: {CropListing.query.count()}")
        print(f"  Vendor Products: {VendorProduct.query.count()}")
        print(f"  Orders: {Order.query.count()}")
        print(f"  Payments: {Payment.query.count()}")
        print(f"  Cost Records: {CostRecord.query.count()}")
        print(f"  Labor Hirings: {LaborHiring.query.count()}")
        print(f"  Equipment: {Equipment.query.count()}")
        print(f"  Equipment Rentals: {EquipmentRental.query.count()}")
        print(f"  Recommendation History: {RecommendationHistory.query.count()}")
        
        # Delete all data (cascade will handle related records)
        print(f"\nDeleting all data...")
        
        # Get all non-admin users
        non_admin_users = User.query.filter(User.role != UserRole.ADMIN).all()
        non_admin_count = len(non_admin_users)
        
        if non_admin_count == 0:
            print("  No demo users to delete.")
        else:
            print(f"  Deleting {non_admin_count} non-admin users and all their data...")
            
            # Delete users (cascade will delete all related data)
            for user in non_admin_users:
                db.session.delete(user)
            
            db.session.commit()
            print(f"  ✓ Deleted {non_admin_count} users")
        
        # Clean up any orphaned orders (orders where buyer no longer exists)
        orphaned_orders = Order.query.filter(~Order.buyer_id.in_(admin_ids)).all()
        if orphaned_orders:
            print(f"  Deleting {len(orphaned_orders)} orphaned orders...")
            for order in orphaned_orders:
                db.session.delete(order)
            db.session.commit()
            print(f"  ✓ Deleted {len(orphaned_orders)} orphaned orders")
        
        # Verify final status
        print(f"\nFinal database status:")
        print(f"  Users: {User.query.count()} (admin only)")
        print(f"  Farmer Profiles: {FarmerProfile.query.count()}")
        print(f"  Vendor Profiles: {VendorProfile.query.count()}")
        print(f"  Labor Profiles: {LaborProfile.query.count()}")
        print(f"  Crop Listings: {CropListing.query.count()}")
        print(f"  Vendor Products: {VendorProduct.query.count()}")
        print(f"  Orders: {Order.query.count()}")
        print(f"  Payments: {Payment.query.count()}")
        print(f"  Cost Records: {CostRecord.query.count()}")
        print(f"  Labor Hirings: {LaborHiring.query.count()}")
        print(f"  Equipment: {Equipment.query.count()}")
        print(f"  Equipment Rentals: {EquipmentRental.query.count()}")
        print(f"  Recommendation History: {RecommendationHistory.query.count()}")
        
        print("\n" + "=" * 60)
        print("✓ Demo data cleanup completed successfully!")
        print("=" * 60)
        print(f"\nRemaining users:")
        remaining_users = User.query.all()
        for user in remaining_users:
            print(f"  - {user.email} ({user.role.value})")

if __name__ == '__main__':
    print("\nWARNING: This will delete ALL demo users and data!")
    print("Only admin accounts will be preserved.")
    response = input("\nDo you want to continue? (yes/no): ")
    
    if response.lower() == 'yes':
        clear_demo_data()
    else:
        print("Operation cancelled.")
