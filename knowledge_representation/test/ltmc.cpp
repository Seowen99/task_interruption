#include <knowledge_representation/LongTermMemoryConduit.h>
#include <iostream>
#include <string>
#include <knowledge_representation/MemoryConduit.h>
#include <knowledge_representation/convenience.h>
#include <knowledge_representation/Concept.h>

#include <gtest/gtest.h>


using std::vector;
using std::string;
using std::cout;
using std::endl;
using knowledge_rep::EntityAttribute;
using knowledge_rep::Concept;

class LTMCTest : public ::testing::Test {
protected:

    LTMCTest() : ltmc(knowledge_rep::get_default_ltmc()) {}

    void SetUp() override {
        ltmc.delete_all_entities();
    }

    knowledge_rep::LongTermMemoryConduit ltmc;
};

class EntityTest : public ::testing::Test {
protected:

    EntityTest() : ltmc(knowledge_rep::get_default_ltmc()), entity(ltmc.add_entity()),
                   concept(ltmc.get_concept("test concept")) {

    }

    void SetUp() override {

    }

    void TearDown() override {
        entity.delete_entity();
    }

    knowledge_rep::LongTermMemoryConduit ltmc;
    knowledge_rep::Entity entity;
    knowledge_rep::Concept concept;
};


// Declare a test
TEST_F(LTMCTest, InitialConfigurationIsValid) {

    ltmc.delete_all_entities();
    // Robot should exist
    EXPECT_TRUE(ltmc.entity_exists(1));
}

TEST_F(LTMCTest, GetConceptWorks) {
    // Get concept returns the one true concept id
    Concept soda = ltmc.get_concept("soda");
    EXPECT_EQ(soda.entity_id, ltmc.get_concept("soda").entity_id);
}

TEST_F(LTMCTest, SQLQueryWorks) {
    vector<EntityAttribute> query_result;
    ltmc.select_query<string>("SELECT * FROM entity_attributes_str", query_result);
}

TEST_F(LTMCTest, ObjectAndConceptNameSpacesAreSeparate) {

    Concept pitcher_con = ltmc.get_concept("soylent pitcher");
    knowledge_rep::Entity pitcher = ltmc.get_object_named("soylent pitcher");
    EXPECT_NE(ltmc.get_object_named("soylent pitcher").entity_id, pitcher_con.entity_id);
    EXPECT_TRUE(ltmc.entity_exists(pitcher.entity_id));
    // Named entity returns the only entity by that name
    EXPECT_EQ(pitcher, ltmc.get_object_named("soylent pitcher"));
}

TEST_F(LTMCTest, CanOnlyAddAttributeOnce) {
    knowledge_rep::Entity drinkable = ltmc.get_concept("drinkable");
    knowledge_rep::Entity can = ltmc.add_entity();

    // Adding a second time should fail
    EXPECT_TRUE(can.add_attribute("is_a", drinkable));
    EXPECT_FALSE(can.add_attribute("is_a", drinkable));
}

TEST_F(LTMCTest, OnlyValidAttributeNamesAllowed) {
    knowledge_rep::Entity can = ltmc.add_entity();
    EXPECT_FALSE(can.add_attribute("not a real attribute", true));
}

TEST_F(EntityTest, DeleteEntityWorks) {
    concept.delete_entity();
    EXPECT_FALSE(concept.is_valid());
    EXPECT_EQ(0, concept.get_attributes().size());
}

TEST_F(EntityTest, RemoveInstancesWorks) {
    entity.make_instance_of(concept);
    concept.remove_instances();
    EXPECT_FALSE(entity.is_valid());
    EXPECT_EQ(0, concept.get_instances().size());
}

TEST_F(LTMCTest, RecursiveRemoveWorks) {
    Concept parent = ltmc.get_concept("parent concept");
    Concept child = ltmc.get_concept("child concept");
    child.add_attribute("is_a", parent);
    knowledge_rep::Entity object = ltmc.add_entity();
    object.add_attribute("instance_of", child);
    parent.remove_instances();
    EXPECT_FALSE(object.is_valid());
}

TEST_F(EntityTest, AddEntityWorks) {
    ASSERT_TRUE(entity.is_valid());
}

TEST_F(EntityTest, StringAttributeWorks) {
    entity.add_attribute("sensed", "test");
    auto attrs = entity.get_attributes("sensed");
    ASSERT_EQ(typeid(string), attrs.at(0).value.type());
    EXPECT_EQ("test", boost::get<string>(attrs.at(0).value));
    EXPECT_TRUE(entity.remove_attribute("sensed"));
}


TEST_F(EntityTest, IntAttributeWorks) {
    entity.add_attribute("sensed", 1);
    auto attrs = entity.get_attributes("sensed");
    ASSERT_EQ(typeid(int), attrs.at(0).value.type());
    EXPECT_EQ(1, boost::get<int>(attrs.at(0).value));
    EXPECT_TRUE(entity.remove_attribute("sensed"));
}

TEST_F(EntityTest, FloatAttributeWorks) {
    entity.add_attribute("sensed", 1.f);
    auto attrs = entity.get_attributes("sensed");
    ASSERT_EQ(typeid(float), attrs.at(0).value.type());
    EXPECT_EQ(1, boost::get<float>(attrs.at(0).value));
    EXPECT_TRUE(entity.remove_attribute("sensed"));
}

TEST_F(EntityTest, BoolAttributeWorks) {
    entity.add_attribute("sensed", true);
    auto attrs = entity.get_attributes("sensed");
    ASSERT_EQ(typeid(bool), attrs.at(0).value.type());
    EXPECT_TRUE(boost::get<bool>(attrs.at(0).value));
    EXPECT_TRUE(entity.remove_attribute("sensed"));

    entity.add_attribute("sensed", false);
    attrs = entity.get_attributes("sensed");
    ASSERT_EQ(typeid(bool), attrs.at(0).value.type());
    EXPECT_FALSE(boost::get<bool>(attrs.at(0).value));
    EXPECT_TRUE(entity.remove_attribute("sensed"));

}

// Run all the tests
int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}